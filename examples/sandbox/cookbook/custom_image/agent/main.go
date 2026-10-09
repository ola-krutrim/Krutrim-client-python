// Command sandbox-agent is the in-sandbox runtime API (Go port of main.py):
// command execution plus file upload/download/list/exists, confined to
// SANDBOX_BASE_DIR. Same routes, payloads and status codes as the Python agent.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"log"
	"math"
	"mime"
	"net"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"
	"unicode/utf8"
)

const (
	healthMessage         = "Sandbox Runtime is active."
	defaultBaseDir        = "/app"
	defaultExecTimeout    = 300 * time.Second
	killedProcessIOGrace  = 5 * time.Second
	shutdownGracePeriod   = 10 * time.Second
	defaultPort           = "8871"
	requestHeaderTimeout  = 30 * time.Second
	maxExecuteRequestSize = 1 << 20
)

var errAccessDenied = errors.New("Access denied: Path must be within the sandbox base directory")

func baseDir() string {
	if v := strings.TrimSpace(os.Getenv("SANDBOX_BASE_DIR")); v != "" {
		return v
	}
	return defaultBaseDir
}

// realpath mirrors os.path.realpath: symlinks in the existing prefix are
// resolved, the non-existent remainder is appended lexically.
func realpath(p string) string {
	if abs, err := filepath.Abs(p); err == nil {
		p = abs
	}
	rest := ""
	for cur := p; ; {
		if resolved, err := filepath.EvalSymlinks(cur); err == nil {
			return filepath.Join(resolved, rest)
		}
		parent := filepath.Dir(cur)
		if parent == cur {
			return p
		}
		rest = filepath.Join(filepath.Base(cur), rest)
		cur = parent
	}
}

// getSafePath resolves filePath under the base directory and rejects
// anything (including symlinks) that escapes it.
func getSafePath(filePath string) (string, error) {
	base := realpath(baseDir())
	full := realpath(filepath.Join(base, strings.TrimLeft(filePath, "/")))
	if base != "/" && full != base && !strings.HasPrefix(full, base+string(filepath.Separator)) {
		return "", errAccessDenied
	}
	return full, nil
}

func execTimeout() time.Duration {
	raw, ok := os.LookupEnv("SANDBOX_EXEC_TIMEOUT_SECONDS")
	if !ok {
		return defaultExecTimeout
	}
	v, err := strconv.ParseFloat(strings.TrimSpace(raw), 64)
	if err != nil || math.IsNaN(v) || math.IsInf(v, 0) || v <= 0 {
		log.Printf("WARNING: Ignoring invalid SANDBOX_EXEC_TIMEOUT_SECONDS=%q; using default of 300 seconds", raw)
		return defaultExecTimeout
	}
	return time.Duration(v * float64(time.Second))
}

// runCommand runs args from the base directory as the leader of a new session
// so a timeout kills the whole process tree, not just the direct child.
func runCommand(args []string, timeout time.Duration) (stdout, stderr string, exitCode int, err error) {
	if len(args) == 0 {
		return "", "", 0, errors.New("empty command")
	}
	cmd := exec.Command(args[0], args[1:]...)
	cmd.Dir = baseDir()
	cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	// Bounds Wait if a killed command left a daemonised grandchild holding the pipes.
	cmd.WaitDelay = killedProcessIOGrace
	var outBuf, errBuf bytes.Buffer
	cmd.Stdout = &outBuf
	cmd.Stderr = &errBuf

	if err := cmd.Start(); err != nil {
		return "", "", 0, err
	}
	done := make(chan error, 1)
	go func() { done <- cmd.Wait() }()

	timer := time.NewTimer(timeout)
	defer timer.Stop()
	select {
	case <-done:
	case <-timer.C:
		_ = syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
		<-done
		return "", "", 0, fmt.Errorf("Command '%s' timed out after %s seconds",
			strings.Join(args, " "), strconv.FormatFloat(timeout.Seconds(), 'f', -1, 64))
	}

	exitCode = cmd.ProcessState.ExitCode()
	// Match Python's returncode: -N when the child was killed by signal N.
	if ws, ok := cmd.ProcessState.Sys().(syscall.WaitStatus); ok && ws.Signaled() {
		exitCode = -int(ws.Signal())
	}
	return outBuf.String(), errBuf.String(), exitCode, nil
}

// unquote mirrors urllib.parse.unquote: valid %XX escapes are decoded,
// malformed ones are kept verbatim, invalid UTF-8 becomes U+FFFD.
func unquote(s string) string {
	if !strings.Contains(s, "%") {
		return s
	}
	var b strings.Builder
	for i := 0; i < len(s); i++ {
		if s[i] == '%' && i+2 < len(s) && isHex(s[i+1]) && isHex(s[i+2]) {
			v, _ := strconv.ParseUint(s[i+1:i+3], 16, 8)
			b.WriteByte(byte(v))
			i += 2
			continue
		}
		b.WriteByte(s[i])
	}
	return strings.ToValidUTF8(b.String(), string(utf8.RuneError))
}

func isHex(c byte) bool {
	return ('0' <= c && c <= '9') || ('a' <= c && c <= 'f') || ('A' <= c && c <= 'F')
}

// contentDisposition matches Starlette's FileResponse header for filename.
func contentDisposition(filename string) string {
	quoted := pyQuote(filename)
	if quoted != filename {
		return "attachment; filename*=utf-8''" + quoted
	}
	return fmt.Sprintf("attachment; filename=%q", filename)
}

// pyQuote mirrors urllib.parse.quote(s) with its default safe set ("/").
func pyQuote(s string) string {
	var b strings.Builder
	for i := 0; i < len(s); i++ {
		c := s[i]
		if ('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z') || ('0' <= c && c <= '9') || strings.IndexByte("_.-~/", c) >= 0 {
			b.WriteByte(c)
		} else {
			fmt.Fprintf(&b, "%%%02X", c)
		}
	}
	return b.String()
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(v)
}

// validationError is a 422 in the shape FastAPI used for request-validation errors.
func validationError(w http.ResponseWriter, field, msg, errType string) {
	writeJSON(w, http.StatusUnprocessableEntity, map[string]any{
		"detail": []map[string]any{{"type": errType, "loc": []string{"body", field}, "msg": msg}},
	})
}

func message(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"message": msg})
}

type executeResponse struct {
	Stdout   string `json:"stdout"`
	Stderr   string `json:"stderr"`
	ExitCode int    `json:"exit_code"`
}

func handleHealth(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok", "message": healthMessage})
}

func handleExecute(w http.ResponseWriter, r *http.Request) {
	data, err := io.ReadAll(io.LimitReader(r.Body, maxExecuteRequestSize))
	if err != nil {
		validationError(w, "command", "JSON decode error", "json_invalid")
		return
	}
	var body any
	if err := json.Unmarshal(data, &body); err != nil {
		validationError(w, "command", "JSON decode error", "json_invalid")
		return
	}
	obj, ok := body.(map[string]any)
	if !ok {
		validationError(w, "command", "Field required", "missing")
		return
	}
	raw, present := obj["command"]
	if !present {
		validationError(w, "command", "Field required", "missing")
		return
	}
	command, ok := raw.(string)
	if !ok {
		validationError(w, "command", "Input should be a valid string", "string_type")
		return
	}

	args, err := shlexSplit(command)
	if err == nil {
		stdout, stderr, code, runErr := runCommand(args, execTimeout())
		if runErr == nil {
			writeJSON(w, http.StatusOK, executeResponse{Stdout: stdout, Stderr: stderr, ExitCode: code})
			return
		}
		err = runErr
	}
	writeJSON(w, http.StatusOK, executeResponse{Stderr: "Failed to execute command: " + err.Error(), ExitCode: 1})
}

func handleUpload(w http.ResponseWriter, r *http.Request) {
	mr, err := r.MultipartReader()
	if err != nil {
		validationError(w, "file", "Field required", "missing")
		return
	}
	for {
		part, err := mr.NextPart()
		if err == io.EOF {
			validationError(w, "file", "Field required", "missing")
			return
		}
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"detail": "There was an error parsing the body"})
			return
		}
		if part.FormName() != "file" {
			part.Close()
			continue
		}
		// Part.FileName() strips directories; the filename carries the destination path.
		_, params, _ := mime.ParseMediaType(part.Header.Get("Content-Disposition"))
		filename, isFile := params["filename"]
		if !isFile {
			validationError(w, "file", "Expected UploadFile", "value_error")
			return
		}
		saveUpload(w, filename, part)
		return
	}
}

func saveUpload(w http.ResponseWriter, filename string, content io.Reader) {
	log.Printf("--- UPLOAD_FILE CALLED: Attempting to save '%s' ---", filename)
	path, err := getSafePath(filename)
	if err != nil {
		message(w, http.StatusForbidden, "Access denied")
		return
	}
	if err := writeFile(path, content); err != nil {
		log.Printf("An error occurred during file upload: %v", err)
		message(w, http.StatusInternalServerError, "File upload failed: "+err.Error())
		return
	}
	message(w, http.StatusOK, fmt.Sprintf("File '%s' uploaded successfully.", filename))
}

func writeFile(path string, content io.Reader) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o777); err != nil {
		return err
	}
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	if _, err := io.Copy(f, content); err != nil {
		f.Close()
		return err
	}
	return f.Close()
}

func handleDownload(w http.ResponseWriter, r *http.Request, encoded string) {
	decoded := unquote(encoded)
	full, err := getSafePath(decoded)
	if err != nil {
		message(w, http.StatusForbidden, "Access denied")
		return
	}
	fi, err := os.Stat(full)
	if err != nil || !fi.Mode().IsRegular() {
		message(w, http.StatusNotFound, "File not found")
		return
	}
	f, err := os.Open(full)
	if err != nil {
		message(w, http.StatusNotFound, "File not found")
		return
	}
	defer f.Close()
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Header().Set("Content-Disposition", contentDisposition(decoded))
	http.ServeContent(w, r, "", fi.ModTime(), f)
}

type listEntry struct {
	Name    string  `json:"name"`
	Size    int64   `json:"size"`
	Type    string  `json:"type"`
	ModTime float64 `json:"mod_time"`
}

func handleList(w http.ResponseWriter, _ *http.Request, encoded string) {
	full, err := getSafePath(unquote(encoded))
	if err != nil {
		message(w, http.StatusForbidden, "Access denied")
		return
	}
	if fi, err := os.Stat(full); err != nil || !fi.IsDir() {
		message(w, http.StatusNotFound, "Path is not a directory")
		return
	}
	dirEntries, err := os.ReadDir(full)
	if err != nil {
		message(w, http.StatusInternalServerError, "List files failed: "+err.Error())
		return
	}
	entries := make([]listEntry, 0, len(dirEntries))
	for _, e := range dirEntries {
		// Follow symlinks for size/type, like DirEntry.stat()/is_dir() in Python.
		st, err := os.Stat(filepath.Join(full, e.Name()))
		if err != nil {
			message(w, http.StatusInternalServerError, "List files failed: "+err.Error())
			return
		}
		kind := "file"
		if st.IsDir() {
			kind = "directory"
		}
		entries = append(entries, listEntry{
			Name:    e.Name(),
			Size:    st.Size(),
			Type:    kind,
			ModTime: float64(st.ModTime().UnixNano()) / 1e9,
		})
	}
	writeJSON(w, http.StatusOK, entries)
}

func handleExists(w http.ResponseWriter, _ *http.Request, encoded string) {
	decoded := unquote(encoded)
	full, err := getSafePath(decoded)
	if err != nil {
		message(w, http.StatusForbidden, "Access denied")
		return
	}
	_, statErr := os.Stat(full)
	writeJSON(w, http.StatusOK, map[string]any{"path": decoded, "exists": statErr == nil})
}

// newHandler routes requests exactly like the Python agent's route table.
func newHandler() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		p := r.URL.Path
		isGet := r.Method == http.MethodGet || r.Method == http.MethodHead
		isPost := r.Method == http.MethodPost

		type pathRoute struct {
			prefix  string
			handler func(http.ResponseWriter, *http.Request, string)
		}
		switch p {
		case "/":
			if isGet {
				handleHealth(w, r)
				return
			}
		case "/execute":
			if isPost {
				handleExecute(w, r)
				return
			}
		case "/upload":
			if isPost {
				handleUpload(w, r)
				return
			}
		default:
			for _, rt := range []pathRoute{
				{"/download/", handleDownload},
				{"/list/", handleList},
				{"/exists/", handleExists},
			} {
				if rest, ok := strings.CutPrefix(p, rt.prefix); ok {
					if !isGet {
						writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"detail": "Method Not Allowed"})
						return
					}
					rt.handler(w, r, rest)
					return
				}
			}
			writeJSON(w, http.StatusNotFound, map[string]string{"detail": "Not Found"})
			return
		}
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"detail": "Method Not Allowed"})
	})
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}
	host := flag.String("host", "0.0.0.0", "listen address")
	flag.StringVar(&port, "port", port, "listen port (defaults to $PORT, then 8871)")
	flag.Parse()

	srv := &http.Server{
		Addr:              net.JoinHostPort(*host, port),
		Handler:           newHandler(),
		ReadHeaderTimeout: requestHeaderTimeout,
	}

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()
	go func() {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), shutdownGracePeriod)
		defer cancel()
		_ = srv.Shutdown(shutdownCtx)
	}()

	log.Printf("sandbox-agent listening on %s (base dir %s)", srv.Addr, baseDir())
	if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatalf("server error: %v", err)
	}
}
