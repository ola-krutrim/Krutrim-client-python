#!/bin/sh
set -eu
cd /tmp && printf 'public class S{public static void main(String[] a){System.out.println(21*2);}}' > S.java
javac S.java
test "$(java S)" = "42"
echo "java: compiled and ran a class"
