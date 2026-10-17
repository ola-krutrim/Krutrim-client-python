#!/bin/sh
set -eu
test "$(bun -e 'console.log(21*2)')" = "42"
echo "bun: executed and produced a result"
