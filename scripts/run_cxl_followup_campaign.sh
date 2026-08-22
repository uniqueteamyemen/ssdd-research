#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="${SSDD_CAMPAIGN_RUN_ID:-cxl-followup-$(date -u +%Y%m%dT%H%M%SZ)}"
RAW_ROOT="${SSDD_RESULTS_DIR:-${ROOT}/.local-results}/controlled-campaign/${RUN_ID}"
SIMCXL_RUN="$RAW_ROOT/simcxl-type3"
PREFLIGHT="$RAW_ROOT/kvm-preflight"
IN_PLACE_DISK="${SSDD_CAMPAIGN_IN_PLACE_DISK:-0}"
ALLOW_IN_PLACE_FULL="${SSDD_CAMPAIGN_ALLOW_IN_PLACE_FULL:-0}"
mkdir -p "$RAW_ROOT"

set +e
"$ROOT/scripts/run_kvm_timing_preflight.sh" "$PREFLIGHT"
preflight_exit=$?
set -e

if [[ "$preflight_exit" == "0" ]]; then
  boot_mode="kvm"
  allow_atomic=0
  performance_branch="pending_retained_roi_confirmation"
else
  boot_mode="atomic"
  allow_atomic=1
  performance_branch="blocked_no_kvm; behavioral_evidence_only"
fi

{
  printf 'campaign_id=%s\n' "$RUN_ID"
  printf 'campaign_spec=controlled validation campaign owner specification 2026-08-22\n'
  printf 'execution_domain=CXL Type-3 simulation\n'
  printf 'boot_mode=%s\n' "$boot_mode"
  printf 'performance_branch=%s\n' "$performance_branch"
  if [[ "$IN_PLACE_DISK" == "1" ]]; then
    printf 'guest_disk_staging=in-place-behavioral-only\n'
  else
    printf 'guest_disk_staging=copied\n'
  fi
  printf 'atomic_cpu_rule=Atomic CPU results are not performance measurements.\n'
  printf 'source_commit='; git -C "$ROOT" rev-parse HEAD
  printf 'started_utc='; date -u +%Y-%m-%dT%H:%M:%SZ
} > "$RAW_ROOT/campaign-manifest.txt"

SSDD_RESULTS_DIR="$RAW_ROOT" \
SSDD_SIMCXL_CASE_SET=full \
SSDD_ALLOW_ATOMIC_BOOT="$allow_atomic" \
SSDD_SIMCXL_IN_PLACE_DISK="$IN_PLACE_DISK" \
SSDD_SIMCXL_ALLOW_IN_PLACE_FULL="$ALLOW_IN_PLACE_FULL" \
"$ROOT/scripts/run_simcxl_type3_matrix.sh" > "$RAW_ROOT/runner.log" 2>&1

"$ROOT/scripts/verify_cxl_followup_campaign.py" \
  --run-dir "$SIMCXL_RUN" \
  --preflight "$PREFLIGHT"

find "$RAW_ROOT" -type f -print0 | sort -z | xargs -0 sha256sum > "$RAW_ROOT/SHA256SUMS"
sha256sum "$RAW_ROOT/SHA256SUMS" > "$RAW_ROOT/SHA256SUMS.sha256"
echo "controlled CXL follow-up completed: $RAW_ROOT"
