#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="${SSDD_RESULTS_DIR:-$ROOT/.local-results/prehardware}"
REFERENCE="$ROOT/reference/python/prehardware_reference.py"
RUST_SOURCE="$ROOT/reference/rust/prehardware_ledger_reference.rs"
RUST_BINARY="$OUTDIR/prehardware_ledger_reference"

export SSDD_RESULTS_DIR="$OUTDIR"
"$ROOT/scripts/run_prehardware_core.sh"
rustc -O "$RUST_SOURCE" -o "$RUST_BINARY"
python3 "$REFERENCE" --mode replay > "$OUTDIR/python-ledger.json"
"$RUST_BINARY" > "$OUTDIR/rust-ledger.json"
python3 "$REFERENCE" \
  --mode compare-cross-language \
  --first "$OUTDIR/python-ledger.json" \
  --second "$OUTDIR/rust-ledger.json" \
  | tee -a "$OUTDIR/run.log"
python3 "$REFERENCE" --mode scale-load | tee -a "$OUTDIR/run.log"

printf 'Pre-hardware extended suite completed. Local output: %s\n' "$OUTDIR"
