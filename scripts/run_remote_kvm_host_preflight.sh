#!/usr/bin/env bash
# Collects host prerequisites from an already-created remote x86_64 host.
# This script never creates a cloud resource, changes a remote machine, or
# installs packages. It records a blocked result when the mandatory KVM host
# predicates are unavailable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="${1:?usage: run_remote_kvm_host_preflight.sh OUTDIR}"
: "${SSDD_REMOTE_HOST:?set SSDD_REMOTE_HOST to the existing SSH host}"
SSDD_REMOTE_USER="${SSDD_REMOTE_USER:-root}"
SSDD_SSH_KEY="${SSDD_SSH_KEY:-}"

mkdir -p "$OUTDIR"
ssh_args=(-o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20)
if [[ -n "$SSDD_SSH_KEY" ]]; then
  ssh_args+=(-i "$SSDD_SSH_KEY")
fi
remote="${SSDD_REMOTE_USER}@${SSDD_REMOTE_HOST}"

git -C "$ROOT" rev-parse HEAD > "$OUTDIR/repository-commit.txt"
printf '%s\n' "$remote" > "$OUTDIR/remote-endpoint.txt"

remote_probe='set -u
printf "timestamp_utc="; date -u +%Y-%m-%dT%H:%M:%SZ
printf "hostname="; hostname
printf "kernel="; uname -srmo
printf "arch="; uname -m
printf "dev_kvm_present="; [[ -e /dev/kvm && -r /dev/kvm && -w /dev/kvm ]] && echo true || echo false
printf "virtualization_flag_present="; grep -Eq "(^flags|^Features).*\b(vmx|svm)\b" /proc/cpuinfo && echo true || echo false
printf "gem5_path="; command -v gem5.opt || command -v gem5 || echo NOT_FOUND
printf "free_bytes="; df -PB1 / | awk "NR==2 {print \$4}"
printf "memory_bytes="; awk "/MemTotal:/ {print \$2 * 1024}" /proc/meminfo
lscpu 2>&1 || true'

ssh "${ssh_args[@]}" "$remote" "bash -s" <<<"$remote_probe" > "$OUTDIR/remote-host-probe.txt"

dev_kvm="$(awk -F= '$1=="dev_kvm_present" {print $2}' "$OUTDIR/remote-host-probe.txt")"
virt_flag="$(awk -F= '$1=="virtualization_flag_present" {print $2}' "$OUTDIR/remote-host-probe.txt")"
gem5_path="$(awk -F= '$1=="gem5_path" {print $2}' "$OUTDIR/remote-host-probe.txt")"

if [[ "$dev_kvm" == true && "$virt_flag" == true ]]; then
  status="host_prerequisites_passed_pending_gem5_kvm_timing_smoke"
  exit_code=0
else
  status="blocked_remote_host_kvm_prerequisites_missing"
  exit_code=20
fi

cat > "$OUTDIR/remote-kvm-preflight.json" <<EOF
{
  "status": "${status}",
  "remote_endpoint": "${remote}",
  "dev_kvm_readable_writable": ${dev_kvm:-false},
  "vmx_or_svm_present": ${virt_flag:-false},
  "remote_gem5_path": "${gem5_path:-NOT_FOUND}",
  "measurement_admission": "A passing remote host preflight is not performance admission. The next gate is an executed gem5 KVM boot followed by an explicit switch to Timing CPU before ROI, resetstats immediately before ROI, dumpstats after ROI, and retained raw outputs.",
  "atomic_cpu_substitution": "prohibited for performance claims"
}
EOF

sha256sum "$OUTDIR"/* > "$OUTDIR/SHA256SUMS"
printf '%s: %s\n' "$status" "$OUTDIR" >&2
exit "$exit_code"
