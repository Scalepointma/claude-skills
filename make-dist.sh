#!/bin/sh
# Build claude.ai-uploadable skill zips into dist/
set -e
cd "$(dirname "$0")"
rm -rf dist && mkdir dist
for d in plugins/*/skills/*; do
  name=$(basename "$d")
  (cd "$(dirname "$d")" && zip -qr "../../../dist/$name.zip" "$name" -x "*__pycache__*" -x "*.DS_Store")
  echo "dist/$name.zip"
done
