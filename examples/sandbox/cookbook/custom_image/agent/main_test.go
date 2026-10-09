package main

import (
	"bytes"
	"encoding/json"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"path/filepath"
	"testing"
)

func runtimeRequest(t *testing.T, method, path string, body io.Reader, contentType string) *httptest.ResponseRecorder {
	t.Helper()
	request := httptest.NewRequest(method, path, body)
	if contentType != "" {
		request.Header.Set("Content-Type", contentType)
	}
	response := httptest.NewRecorder()
	newHandler().ServeHTTP(response, request)
	return response
}

func uploadRequest(t *testing.T, filename string, content []byte) *httptest.ResponseRecorder {
	t.Helper()
	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	part, err := writer.CreateFormFile("file", filename)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := part.Write(content); err != nil {
		t.Fatal(err)
	}
	if err := writer.Close(); err != nil {
		t.Fatal(err)
	}
	return runtimeRequest(t, http.MethodPost, "/upload", &body, writer.FormDataContentType())
}

func requireStatus(t *testing.T, response *httptest.ResponseRecorder, want int) {
	t.Helper()
	if response.Code != want {
		t.Fatalf("status = %d, want %d; body = %s", response.Code, want, response.Body.String())
	}
}

func decodeResponse(t *testing.T, response *httptest.ResponseRecorder, destination any) {
	t.Helper()
	if err := json.Unmarshal(response.Body.Bytes(), destination); err != nil {
		t.Fatal(err)
	}
}

func TestHealth(t *testing.T) {
	response := runtimeRequest(t, http.MethodGet, "/", nil, "")
	requireStatus(t, response, http.StatusOK)
	var health map[string]string
	decodeResponse(t, response, &health)
	if health["status"] != "ok" || health["message"] != "Sandbox Runtime is active." {
		t.Fatalf("unexpected health response: %v", health)
	}
}

func TestExecute(t *testing.T) {
	t.Setenv("SANDBOX_BASE_DIR", t.TempDir())
	t.Setenv("SANDBOX_EXEC_TIMEOUT_SECONDS", "5")
	tests := []struct {
		name     string
		command  string
		stdout   string
		stderr   string
		exitCode int
	}{
		{"quoted arguments", `printf '%s|%s|%s' 'hello world' "double quoted" escaped\ space`, "hello world|double quoted|escaped space", "", 0},
		{"empty argument", `printf '<%s>' ""`, "<>", "", 0},
		{"nonzero exit", `sh -c 'printf output; printf error >&2; exit 7'`, "output", "error", 7},
		{"unclosed quote", `printf 'unfinished`, "", "Failed to execute command: No closing quotation", 1},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			body, err := json.Marshal(map[string]string{"command": test.command})
			if err != nil {
				t.Fatal(err)
			}
			response := runtimeRequest(t, http.MethodPost, "/execute", bytes.NewReader(body), "application/json")
			requireStatus(t, response, http.StatusOK)
			var result executeResponse
			decodeResponse(t, response, &result)
			if result.Stdout != test.stdout || result.Stderr != test.stderr || result.ExitCode != test.exitCode {
				t.Fatalf("unexpected execution result: %+v", result)
			}
		})
	}
}

func TestFileRoundTrip(t *testing.T) {
	base := t.TempDir()
	t.Setenv("SANDBOX_BASE_DIR", base)
	filename := "nested/hello world.bin"
	content := []byte{'h', 'i', '\n', 0, 255}
	requireStatus(t, uploadRequest(t, filename, content), http.StatusOK)
	stored, err := os.ReadFile(filepath.Join(base, filename))
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(stored, content) {
		t.Fatalf("uploaded bytes = %v, want %v", stored, content)
	}

	download := runtimeRequest(t, http.MethodGet, "/download/"+url.PathEscape(filename), nil, "")
	requireStatus(t, download, http.StatusOK)
	if !bytes.Equal(download.Body.Bytes(), content) {
		t.Fatalf("downloaded bytes = %v, want %v", download.Body.Bytes(), content)
	}
	if download.Header().Get("Content-Disposition") == "" {
		t.Fatal("missing download Content-Disposition")
	}

	listing := runtimeRequest(t, http.MethodGet, "/list/nested", nil, "")
	requireStatus(t, listing, http.StatusOK)
	var entries []listEntry
	decodeResponse(t, listing, &entries)
	if len(entries) != 1 || entries[0].Name != "hello world.bin" || entries[0].Size != int64(len(content)) || entries[0].Type != "file" || entries[0].ModTime <= 0 {
		t.Fatalf("unexpected listing: %+v", entries)
	}

	for _, test := range []struct {
		path   string
		exists bool
	}{{filename, true}, {"missing.bin", false}} {
		response := runtimeRequest(t, http.MethodGet, "/exists/"+url.PathEscape(test.path), nil, "")
		requireStatus(t, response, http.StatusOK)
		var result struct {
			Path   string `json:"path"`
			Exists bool   `json:"exists"`
		}
		decodeResponse(t, response, &result)
		if result.Path != test.path || result.Exists != test.exists {
			t.Fatalf("unexpected exists response: %+v", result)
		}
	}
	requireStatus(t, runtimeRequest(t, http.MethodGet, "/download/missing.bin", nil, ""), http.StatusNotFound)
	requireStatus(t, runtimeRequest(t, http.MethodGet, "/list/"+url.PathEscape(filename), nil, ""), http.StatusNotFound)
}

func TestPathTraversalRejected(t *testing.T) {
	root := t.TempDir()
	base := filepath.Join(root, "sandbox")
	outside := filepath.Join(root, "outside")
	if err := os.MkdirAll(base, 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(outside, 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(outside, "secret.txt"), []byte("secret"), 0o600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(outside, filepath.Join(base, "escape")); err != nil {
		t.Fatal(err)
	}
	t.Setenv("SANDBOX_BASE_DIR", base)
	for _, path := range []string{"../outside/secret.txt", "%2e%2e%2foutside%2fsecret.txt", "escape/secret.txt"} {
		for _, route := range []string{"/download/", "/list/", "/exists/"} {
			t.Run(route+path, func(t *testing.T) {
				response := runtimeRequest(t, http.MethodGet, route+path, nil, "")
				requireStatus(t, response, http.StatusForbidden)
			})
		}
	}
	for _, path := range []string{"../outside/new.txt", "escape/new.txt"} {
		requireStatus(t, uploadRequest(t, path, []byte("must not escape")), http.StatusForbidden)
	}
	if _, err := os.Stat(filepath.Join(outside, "new.txt")); !os.IsNotExist(err) {
		t.Fatalf("rejected upload created an outside file: %v", err)
	}
}
