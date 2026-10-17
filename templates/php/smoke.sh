#!/bin/sh
set -eu
test "$(php -r 'echo 21*2;')" = "42"
echo "php: executed and produced a result"
