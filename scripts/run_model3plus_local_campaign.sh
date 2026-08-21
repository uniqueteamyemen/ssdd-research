#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_LABEL="${SSDD_MODEL3_RUN_LABEL:-model3plus-local-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTDIR="${SSDD_RESULTS_DIR:-$ROOT/.local-results/$RUN_LABEL}"
REFERENCE="$ROOT/reference/python/prehardware_reference.py"
RUST_SOURCE="$ROOT/reference/rust/prehardware_ledger_reference.rs"
WORKLOAD_SOURCE="$ROOT/simulation/gem5/ssdd_reference_workload.cpp"
VERIFY="$ROOT/scripts/verify_model3plus_local_campaign.py"

[[ "$OUTDIR" == "$ROOT/.local-results/"* ]] || {
  echo "refusing output outside $ROOT/.local-results/: $OUTDIR" >&2
  exit 64
}
[[ ! -e "$OUTDIR" ]] || {
  echo "refusing to overwrite existing evidence directory: $OUTDIR" >&2
  exit 64
}

for command in python3 rustc g++ sha256sum git; do
  command -v "$command" >/dev/null || {
    echo "setup-blocked: required command unavailable: $command" >&2
    exit 20
  }
done

for path in "$REFERENCE" "$RUST_SOURCE" "$WORKLOAD_SOURCE" "$VERIFY"; do
  [[ -f "$path" ]] || {
    echo "setup-blocked: required source unavailable: $path" >&2
    exit 20
  }
done

mkdir -p "$OUTDIR/prehardware"

{
  printf 'campaign=SSDD Model 3+ local evidence packages A-E\n'
  printf 'campaign_scope=behavioral_and_integrity_reference_only\n'
  printf 'started_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'repository_commit=%s\n' "$(git -C "$ROOT" rev-parse HEAD)"
  printf 'repository_status=%s\n' "$(git -C "$ROOT" -c color.status=never status --short | tr '\n' ';' || true)"
  printf 'python=%s\n' "$(python3 --version)"
  printf 'rustc=%s\n' "$(rustc --version)"
  printf 'gxx=%s\n' "$(g++ --version | head -n 1)"
  printf 'host_kernel=%s\n' "$(uname -srmo)"
  printf 'kvm_available=%s\n' "$([[ -e /dev/kvm ]] && echo true || echo false)"
  printf 'performance_measurement=false\n'
  printf 'hardware_claim=false\n'
  printf 'external_access=false\n'
} > "$OUTDIR/run-manifest.txt"

{
  sha256sum "$REFERENCE"
  sha256sum "$RUST_SOURCE"
  sha256sum "$WORKLOAD_SOURCE"
  sha256sum "$ROOT/scripts/run_prehardware_core.sh"
  sha256sum "$ROOT/scripts/run_model3plus_local_campaign.sh"
  sha256sum "$VERIFY"
  sha256sum "$ROOT/docs/validation/adversarial-validation-plan.md"
  sha256sum "$ROOT/docs/validation/verification-matrix.md"
  sha256sum "$ROOT/docs/validation/model3plus-local-campaign-plan.md"
} > "$OUTDIR/source-register.sha256"

run() {
  printf '\n+ %q' "$@" | tee -a "$OUTDIR/run.log"
  printf '\n' | tee -a "$OUTDIR/run.log"
  "$@" 2>&1 | tee -a "$OUTDIR/run.log"
}

export SSDD_RESULTS_DIR="$OUTDIR/prehardware"
run "$ROOT/scripts/run_prehardware_core.sh"

RUST_BINARY="$OUTDIR/prehardware/prehardware_ledger_reference"
run rustc -O "$RUST_SOURCE" -o "$RUST_BINARY"
run bash -c 'python3 "$1" --mode replay > "$2"' _ "$REFERENCE" "$OUTDIR/prehardware/python-ledger.json"
run bash -c '"$1" > "$2"' _ "$RUST_BINARY" "$OUTDIR/prehardware/rust-ledger.json"
run python3 "$REFERENCE" --mode compare-cross-language \
  --first "$OUTDIR/prehardware/python-ledger.json" \
  --second "$OUTDIR/prehardware/rust-ledger.json"

WORKLOAD_BINARY="$OUTDIR/proof-integrity-workload"
run g++ -O2 -std=c++20 "$WORKLOAD_SOURCE" -o "$WORKLOAD_BINARY"
run bash -c '"$1" --fault=none > "$2"' _ "$WORKLOAD_BINARY" "$OUTDIR/proof-accepted.txt"

set +e
printf '\n+ %q' "$WORKLOAD_BINARY" '--fault=proof-corruption' '--fault-record=18' | tee -a "$OUTDIR/run.log"
printf '\n' | tee -a "$OUTDIR/run.log"
"$WORKLOAD_BINARY" --fault=proof-corruption --fault-record=18 \
  > "$OUTDIR/proof-corruption.txt" 2>&1
proof_exit=$?
cat "$OUTDIR/proof-corruption.txt" | tee -a "$OUTDIR/run.log"
set -e
printf 'proof_corruption_exit=%s\n' "$proof_exit" >> "$OUTDIR/run-manifest.txt"
[[ "$proof_exit" -eq 2 ]] || {
  echo "proof-corruption did not produce the predeclared rejection exit code" >&2
  exit 1
}

run python3 "$VERIFY" --outdir "$OUTDIR"

printf 'completed_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUTDIR/run-manifest.txt"
find "$OUTDIR" -type f ! -name 'SHA256SUMS' ! -name 'SHA256SUMS.sha256' -print0 \
  | sort -z \
  | xargs -0 sha256sum > "$OUTDIR/SHA256SUMS"
sha256sum "$OUTDIR/SHA256SUMS" > "$OUTDIR/SHA256SUMS.sha256"

echo "Model 3+ local A-E campaign accepted. Local output: $OUTDIR"
