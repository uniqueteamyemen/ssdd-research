#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="${1:-concurrent-local-policy-$(date -u +%Y%m%dT%H%M%SZ)}"
OUT="${SSDD_COMPARATIVE_RESULTS_DIR:-$ROOT/evidence/comparative/$LABEL}"
mkdir -p "$OUT"

{
  printf 'command: python3 comparison/concurrent_policy_matrix.py --output %q --run-label %q\n' "$OUT" "$LABEL"
  printf 'host: '; hostname
  printf 'utc: '; date -u +%FT%TZ
  printf 'research_commit: '; git -C "$ROOT" rev-parse HEAD
  printf 'matrix_sha256: '; sha256sum "$ROOT/comparison/concurrent_policy_matrix.py" | cut -d' ' -f1
  printf 'runner_sha256: '; sha256sum "$ROOT/scripts/run_ssdd_comparative_concurrent_native.sh" | cut -d' ' -f1
  printf 'python: '; python3 --version
} > "$OUT/provenance.txt"

python3 "$ROOT/comparison/concurrent_policy_matrix.py" --output "$OUT" --run-label "$LABEL" > "$OUT/stdout.log" 2> "$OUT/stderr.log"
(
  cd "$OUT"
  find . -type f ! -name 'SHA256SUMS' ! -name 'checksum-verification.txt' -printf '%P\n' | sort | while IFS= read -r file; do sha256sum "$file"; done > SHA256SUMS
  sha256sum -c SHA256SUMS > checksum-verification.txt
)
printf '%s\n' "$OUT"
