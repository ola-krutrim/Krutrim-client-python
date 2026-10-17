#!/bin/sh
# Must produce a linked binary and run it — the exact thing a missing cc breaks.
set -eu
cd /tmp
cargo new smoke -q
cd smoke
cargo build -q
./target/debug/smoke | grep -q "Hello, world!"
echo "rust: built and ran a binary"
