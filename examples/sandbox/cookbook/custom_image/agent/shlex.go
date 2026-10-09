package main

import (
	"errors"
	"strings"
)

// shlexSplit splits a command line like Python's shlex.split (POSIX mode,
// whitespace_split, no comments), so /execute tokenizes exactly as before.
func shlexSplit(s string) ([]string, error) {
	var (
		tokens  []string
		cur     strings.Builder
		inToken bool
	)
	runes := []rune(s)
	for i := 0; i < len(runes); i++ {
		c := runes[i]
		switch {
		case c == ' ' || c == '\t' || c == '\r' || c == '\n':
			if inToken {
				tokens = append(tokens, cur.String())
				cur.Reset()
				inToken = false
			}
		case c == '\\':
			if i+1 >= len(runes) {
				return nil, errors.New("No escaped character")
			}
			i++
			cur.WriteRune(runes[i])
			inToken = true
		case c == '\'':
			inToken = true
			end := indexRune(runes, i+1, '\'')
			if end < 0 {
				return nil, errors.New("No closing quotation")
			}
			cur.WriteString(string(runes[i+1 : end]))
			i = end
		case c == '"':
			inToken = true
			i++
			for ; ; i++ {
				if i >= len(runes) {
					return nil, errors.New("No closing quotation")
				}
				if runes[i] == '"' {
					break
				}
				// Inside double quotes a backslash only escapes '"' and '\'.
				if runes[i] == '\\' {
					if i+1 >= len(runes) {
						return nil, errors.New("No closing quotation")
					}
					if next := runes[i+1]; next == '"' || next == '\\' {
						cur.WriteRune(next)
						i++
						continue
					}
				}
				cur.WriteRune(runes[i])
			}
		default:
			cur.WriteRune(c)
			inToken = true
		}
	}
	if inToken {
		tokens = append(tokens, cur.String())
	}
	return tokens, nil
}

func indexRune(runes []rune, from int, r rune) int {
	for i := from; i < len(runes); i++ {
		if runes[i] == r {
			return i
		}
	}
	return -1
}
