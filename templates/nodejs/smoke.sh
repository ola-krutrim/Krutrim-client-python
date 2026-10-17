#!/bin/sh
set -eu
test "$(node -e 'console.log(21*2)')" = "42"
echo "nodejs: executed and produced a result"
