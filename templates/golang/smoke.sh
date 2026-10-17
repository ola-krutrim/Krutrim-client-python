#!/bin/sh
set -eu
cd /tmp && mkdir -p smoke && cd smoke
printf 'package main\nimport "fmt"\nfunc main(){fmt.Println(21*2)}\n' > main.go
go mod init smoke >/dev/null 2>&1 || true
go build -o prog main.go
test "$(./prog)" = "42"
echo "golang: compiled and ran a binary"
