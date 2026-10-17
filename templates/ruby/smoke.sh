#!/bin/sh
set -eu
test "$(ruby -e 'puts 21*2')" = "42"
echo "ruby: executed and produced a result"
