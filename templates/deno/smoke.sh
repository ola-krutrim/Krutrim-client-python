#!/bin/sh
set -eu
test "$(deno eval 'console.log(21*2)')" = "42"
echo "deno: executed and produced a result"
