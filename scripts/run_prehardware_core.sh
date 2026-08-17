#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="${SSDD_RESULTS_DIR:-$ROOT/.local-results/prehardware}"
REFERENCE="$ROOT/reference/python/prehardware_reference.py"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"
export SSDD_RESULTS_DIR="$OUTDIR"

python3 "$REFERENCE" --mode core | tee "$OUTDIR/run.log"
python3 "$REFERENCE" --mode replay > "$OUTDIR/replay-independent-a.json"
python3 "$REFERENCE" --mode replay > "$OUTDIR/replay-independent-b.json"
python3 "$REFERENCE" \
  --mode compare-replays \
  --first "$OUTDIR/replay-independent-a.json" \
  --second "$OUTDIR/replay-independent-b.json" \
  | tee -a "$OUTDIR/run.log"

printf 'Pre-hardware core suite completed. Local output: %s\n' "$OUTDIR"
