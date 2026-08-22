#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="${1:?usage: run_kvm_timing_preflight.sh OUTDIR}"
mkdir -p "$OUTDIR"

has_kvm=false
has_virtualization_flag=false
if [[ -e /dev/kvm && -r /dev/kvm && -w /dev/kvm ]]; then
  has_kvm=true
fi
if grep -Eq '(^flags|^Features).*\b(vmx|svm)\b' /proc/cpuinfo; then
  has_virtualization_flag=true
fi

git -C "$ROOT" rev-parse HEAD > "$OUTDIR/repository-commit.txt"
uname -a > "$OUTDIR/uname.txt"
lscpu > "$OUTDIR/lscpu.txt" 2>&1 || true
{
  printf 'timestamp_utc='; date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'repository_commit='; cat "$OUTDIR/repository-commit.txt"
  printf 'dev_kvm_present=%s\n' "$has_kvm"
  printf 'virtualization_flag_present=%s\n' "$has_virtualization_flag"
  printf 'measurement_rule=KVM boot plus Timing CPU ROI is mandatory for latency,jitter,throughput,overhead,scaling,contention,and recovery timing.\n'
} > "$OUTDIR/preflight-manifest.txt"

if [[ "$has_kvm" == true && "$has_virtualization_flag" == true ]]; then
  status="host_prerequisites_passed_pending_gem5_kvm_timing_smoke"
  exit_code=0
else
  status="blocked_host_kvm_prerequisites_missing"
  exit_code=20
fi

cat > "$OUTDIR/kvm-preflight.json" <<EOF
{
  "status": "${status}",
  "dev_kvm_readable_writable": ${has_kvm},
  "vmx_or_svm_present": ${has_virtualization_flag},
  "measurement_admission": "A host preflight is not a performance admission. Admission requires a successful gem5 KVM boot, an explicit switch to Timing CPU before ROI, and retained resetstats/dumpstats boundaries.",
  "atomic_cpu_substitution": "prohibited for performance claims"
}
EOF

sha256sum "$OUTDIR"/* > "$OUTDIR/SHA256SUMS"
echo "${status}: $OUTDIR" >&2
exit "$exit_code"
