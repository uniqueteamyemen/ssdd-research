#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${1:?usage: create_ssdd_comparative_reviewer_packets.sh <comparative-evidence-dir> <review-output-dir>}"
OUT="${2:?usage: create_ssdd_comparative_reviewer_packets.sh <comparative-evidence-dir> <review-output-dir>}"

rm -rf "$OUT"
python3 "$ROOT/comparison/create_blinded_reviewer_packets.py" --source "$SOURCE" --output "$OUT"
(
  cd "$OUT"
  find . -type f ! -name 'SHA256SUMS' ! -name 'checksum-verification.txt' -printf '%P\n' | sort | while IFS= read -r file; do sha256sum "$file"; done > SHA256SUMS
  sha256sum -c SHA256SUMS > checksum-verification.txt
)
printf '%s\n' "$OUT"
