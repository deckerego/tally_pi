#!/usr/bin/env bash

if [[ -z "$1" ]]; then
  echo "Usage: $0 NETWORK"
  echo "Example: $0 192.168.1"
  exit -1
fi

PREFIX="$1"

echo -n "Searching through $PREFIX "
for SUFFIX in {2..254}; do
  echo -n "."
  nc -z -v -G 1 "$PREFIX.$SUFFIX" 7413 &>/dev/null
  if [[ $? -eq 0 ]]; then
    echo
    echo "Found light at $PREFIX.$SUFFIX"
  fi
done

echo
echo "Done searching."
