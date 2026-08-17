#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5_ROOT="${GEM5_ROOT:?Set GEM5_ROOT to a compatible gem5 checkout. gem5 is intentionally not bundled.}"
GEM5="$GEM5_ROOT/build/X86/gem5.opt"
SRC="$ROOT/simulation/gem5/ssdd_reference_workload.cpp"
CONFIG="$ROOT/simulation/gem5/controlled_se.py"
OUTROOT="${SSDD_RESULTS_DIR:-$ROOT/.local-results}/gem5-controlled-matrix"
BIN="$OUTROOT/ssdd_reference_workload"

[[ -x "$GEM5" ]] || { echo "Missing gem5 binary: $GEM5" >&2; exit 2; }
mkdir -p "$OUTROOT"
g++ -O2 -std=c++20 -static "$SRC" -o "$BIN"

run_case() {
  local case_name="$1" latency="$2" fault="$3" attempt="$4" fault_record="${5:-18}"
  local target="$OUTROOT/${case_name}/run-${attempt}"
  mkdir -p "$target"
  set +e
  "$GEM5" -d "$target" --redirect-stdout --stdout-file=simout "$CONFIG" \
    --cmd="$BIN" --options="--fault=${fault} --fault-record=${fault_record}" \
    --cpu-type=TimingSimpleCPU --mem-type=SimpleMemory --ssdd-memory-latency="$latency" \
    --mem-size=256MB --caches --l1d_size=32kB --l1i_size=32kB
  local gem5_exit=$?
  set -e
  grep -E '^(stages|replay_digest|reference_digest|memory_probe|fault_mode|fault_record|validation)=' "$target/simout" > "$target/summary"
  grep -E '^simTicks[[:space:]]+' "$target/stats.txt" | head -1 > "$target/sim_ticks"
  printf 'gem5_exit=%s\n' "$gem5_exit" >> "$target/summary"
}

for latency in 10ns 50ns 100ns; do
  for attempt in 1 2; do run_case "latency-${latency}" "$latency" none "$attempt"; done
  diff -u "$OUTROOT/latency-${latency}/run-1/summary" "$OUTROOT/latency-${latency}/run-2/summary"
done
for fault in none proof-corruption; do
  for attempt in 1 2; do run_case "fault-${fault}" 50ns "$fault" "$attempt" 18; done
  diff -u "$OUTROOT/fault-${fault}/run-1/summary" "$OUTROOT/fault-${fault}/run-2/summary"
done
for attempt in 1 2 3 4 5; do run_case replay-50ns 50ns none "$attempt" 18; done
for attempt in 2 3 4 5; do diff -u "$OUTROOT/replay-50ns/run-1/summary" "$OUTROOT/replay-50ns/run-${attempt}/summary"; done
for fault_record in 1 18 35; do
  for attempt in 1 2; do run_case "fault-proof-corruption-record-${fault_record}" 50ns proof-corruption "$attempt" "$fault_record"; done
  diff -u "$OUTROOT/fault-proof-corruption-record-${fault_record}/run-1/summary" "$OUTROOT/fault-proof-corruption-record-${fault_record}/run-2/summary"
done
{
  printf 'case,latency_ns,attempt,validation,replay_digest,reference_digest,memory_probe,sim_ticks,gem5_exit\n'
  for summary in "$OUTROOT"/*/run-*/summary; do
    run_dir="$(dirname "$summary")"; case_name="$(basename "$(dirname "$run_dir")")"; attempt="$(basename "$run_dir" | sed 's/run-//')"
    latency_ns="${case_name#latency-}"; [[ "$case_name" == fault-* || "$case_name" == replay-* ]] && latency_ns=50ns
    printf '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' "$case_name" "$latency_ns" "$attempt" \
      "$(awk -F= '/^validation=/{print $2}' "$summary")" "$(awk -F= '/^replay_digest=/{print $2}' "$summary")" \
      "$(awk -F= '/^reference_digest=/{print $2}' "$summary")" "$(awk -F= '/^memory_probe=/{print $2}' "$summary")" \
      "$(awk '{print $2}' "$run_dir/sim_ticks")" "$(awk -F= '/^gem5_exit=/{print $2}' "$summary")"
  done
} > "$OUTROOT/matrix.csv"
printf 'gem5 controlled matrix completed. Local output: %s\n' "$OUTROOT"
