#!/usr/bin/env bash
# Run the bounded SSC RTL simulation. This is not FPGA or CXL validation.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${SSDD_RTL_RESULTS_DIR:-$ROOT/evidence/rtl-ssc}"
MODULE="$ROOT/rtl/ssc/snapshot_epoch_ssc.sv"
TESTBENCH="$ROOT/rtl/ssc/tb_snapshot_epoch_ssc.sv"
REFERENCE="$ROOT/reference/python/rtl_ssc_vector_reference.py"

command -v iverilog >/dev/null || {
  echo "missing prerequisite: iverilog" >&2
  exit 2
}
command -v vvp >/dev/null || {
  echo "missing prerequisite: vvp" >&2
  exit 2
}

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
for run in 1 2; do
  run_dir="$OUT_DIR/run-$run"
  mkdir -p "$run_dir"
  iverilog -g2012 -Wall -s tb_snapshot_epoch_ssc -o "$run_dir/rtl_ssc.vvp" "$MODULE" "$TESTBENCH"
  vvp "$run_dir/rtl_ssc.vvp" | tee "$run_dir/simulation.log"
  grep -q '^RTL_SSC_RESULT status=PASS$' "$run_dir/simulation.log"
  python3 "$REFERENCE" --log "$run_dir/simulation.log" --expected-json "$run_dir/reference-vector.json" | tee "$run_dir/reference-compare.log"
done

cmp -s "$OUT_DIR/run-1/simulation.log" "$OUT_DIR/run-2/simulation.log" || {
  echo "independent RTL simulation logs differ" >&2
  exit 1
}
cp "$OUT_DIR/run-1/simulation.log" "$OUT_DIR/simulation.log"

module_hash="$(sha256sum "$MODULE" | awk '{print $1}')"
testbench_hash="$(sha256sum "$TESTBENCH" | awk '{print $1}')"
log_hash="$(sha256sum "$OUT_DIR/simulation.log" | awk '{print $1}')"
reference_hash="$(sha256sum "$OUT_DIR/run-1/reference-vector.json" | awk '{print $1}')"
run_one_hash="$(sha256sum "$OUT_DIR/run-1/simulation.log" | awk '{print $1}')"
run_two_hash="$(sha256sum "$OUT_DIR/run-2/simulation.log" | awk '{print $1}')"
cat > "$OUT_DIR/manifest.json" <<EOF
{
  "domain": "rtl_simulation",
  "tool": "Icarus Verilog $(iverilog -V 2>&1 | head -n 1 | sed 's/"/\\"/g')",
  "module": "rtl/ssc/snapshot_epoch_ssc.sv",
  "testbench": "rtl/ssc/tb_snapshot_epoch_ssc.sv",
  "accepted_cases": [
    "128 deterministic affine arrival-order trials across 32 complete unique permutations",
    "three-key-prefix source-chiplet tie break",
    "exact four-key collision rejection",
    "valid snapshot recovery after rejection",
    "two independent simulator invocations with byte-identical traces",
    "independent Python trace-vector comparison"
  ],
  "sha256": {
    "module": "$module_hash",
    "testbench": "$testbench_hash",
    "simulation_log": "$log_hash",
    "reference_vector": "$reference_hash",
    "run_1_log": "$run_one_hash",
    "run_2_log": "$run_two_hash"
  },
  "limitations": "Behavioral RTL simulation only. No aggregation, state hash, CXL traffic, synthesis, timing closure, FPGA, real hardware, or production-runtime claim is made."
}
EOF
printf 'RTL SSC evidence: %s\n' "$OUT_DIR/manifest.json"
