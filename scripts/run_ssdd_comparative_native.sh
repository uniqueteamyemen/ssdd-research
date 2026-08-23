#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="${1:-native-contract-smoke-$(date -u +%Y%m%dT%H%M%SZ)}"
OUT="${SSDD_COMPARATIVE_RESULTS_DIR:-$ROOT/evidence/comparative/$LABEL}"

mkdir -p "$OUT"
{
  printf 'command: python3 comparison/ssdd_comparative_harness.py --output %q --run-label %q\n' "$OUT" "$LABEL"
  printf 'host: '; hostname
  printf 'utc: '; date -u +%FT%TZ
  printf 'research_commit: '; git -C "$ROOT" rev-parse HEAD
  printf 'harness_sha256: '; sha256sum "$ROOT/comparison/ssdd_comparative_harness.py" | cut -d' ' -f1
  printf 'runner_sha256: '; sha256sum "$ROOT/scripts/run_ssdd_comparative_native.sh" | cut -d' ' -f1
  printf 'python: '; python3 --version
} > "$OUT/provenance.txt"

python3 "$ROOT/comparison/ssdd_comparative_harness.py" --output "$OUT" --run-label "$LABEL" \
  > "$OUT/stdout.log" 2> "$OUT/stderr.log"

(
  cd "$OUT"
  find . -type f ! -name 'SHA256SUMS' ! -name 'checksum-verification.txt' -printf '%P\n' \
    | sort \
    | while IFS= read -r file; do sha256sum "$file"; done > SHA256SUMS
)

(
  cd "$OUT"
  sha256sum -c SHA256SUMS
) > "$OUT/checksum-verification.txt"

printf '%s\n' "$OUT"
