#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5_ROOT="${GEM5_ROOT:?Set GEM5_ROOT to a compatible gem5 checkout. gem5 is intentionally not bundled.}"
GEM5="$GEM5_ROOT/build/X86/gem5.opt"
CONFIG="$GEM5_ROOT/configs/deprecated/example/se.py"
SRC="$ROOT/simulation/gem5/ssdd_reference_workload.cpp"
OUTROOT="${SSDD_RESULTS_DIR:-$ROOT/.local-results}/gem5-baseline"
BIN="$OUTROOT/ssdd_reference_workload"

[[ -x "$GEM5" ]] || { echo "Missing gem5 binary: $GEM5" >&2; exit 2; }
[[ -f "$CONFIG" ]] || { echo "Missing gem5 configuration: $CONFIG" >&2; exit 2; }
mkdir -p "$OUTROOT"
g++ -O2 -std=c++20 -static "$SRC" -o "$BIN"

for run in one two; do
  "$GEM5" -d "$OUTROOT/$run" --redirect-stdout --stdout-file=simout "$CONFIG" \
    --cmd="$BIN" --cpu-type=TimingSimpleCPU --mem-size=256MB --caches \
    --l1d_size=32kB --l1i_size=32kB
done

grep -E '^(stages|replay_digest|validation)=' "$OUTROOT/one/simout" > "$OUTROOT/one.summary"
grep -E '^(stages|replay_digest|validation)=' "$OUTROOT/two/simout" > "$OUTROOT/two.summary"
diff -u "$OUTROOT/one.summary" "$OUTROOT/two.summary"
printf 'gem5 baseline replay passed. Local output: %s\n' "$OUTROOT"
