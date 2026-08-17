#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SIMCXL_ROOT="${SIMCXL_ROOT:?Set SIMCXL_ROOT to the selected SimCXL checkout.}"
SIMCXL_KERNEL="${SIMCXL_KERNEL:?Set SIMCXL_KERNEL to a CXL-aware full-system kernel.}"
SIMCXL_DISK="${SIMCXL_DISK:?Set SIMCXL_DISK to a compatible full-system disk image.}"
SIMCXL_BIN="${SIMCXL_ROOT}/build/X86/gem5.opt"
CONFIG="${ROOT}/simulation/cxl/simcxl_type3_ssdd.py"
SOURCE="${ROOT}/simulation/gem5/ssdd_reference_workload.cpp"
GUEST_SERVICE="${ROOT}/simulation/cxl/guest/ssdd-gem5-readfile.service"
OUTROOT="${SSDD_RESULTS_DIR:-${ROOT}/.local-results}/simcxl-type3"
CASE_SET="${SSDD_SIMCXL_CASE_SET:-limited}"
ALLOW_ATOMIC_BOOT="${SSDD_ALLOW_ATOMIC_BOOT:-0}"
IN_PLACE_DISK="${SSDD_SIMCXL_IN_PLACE_DISK:-0}"

for path in "$SIMCXL_ROOT" "$SIMCXL_KERNEL" "$SIMCXL_DISK" "$SIMCXL_BIN" "$CONFIG" "$SOURCE" "$GUEST_SERVICE"; do
  [[ -e "$path" ]] || { echo "setup-blocked: missing required path: $path" >&2; exit 20; }
done
[[ -x "$SIMCXL_BIN" ]] || { echo "setup-blocked: SimCXL binary is not executable: $SIMCXL_BIN" >&2; exit 20; }
command -v debugfs >/dev/null || { echo "setup-blocked: debugfs is required to stage the guest binary" >&2; exit 20; }
command -v losetup >/dev/null || { echo "setup-blocked: losetup is required for partitioned guest disks" >&2; exit 20; }

if [[ -e /dev/kvm ]]; then
  BOOT_CPU=kvm
elif [[ "$ALLOW_ATOMIC_BOOT" == "1" ]]; then
  BOOT_CPU=atomic
  echo "warning: /dev/kvm is unavailable; using explicitly allowed atomic boot" >&2
else
  echo "setup-blocked: /dev/kvm unavailable; set SSDD_ALLOW_ATOMIC_BOOT=1 to permit a substantially slower atomic boot" >&2
  exit 20
fi

mkdir -p "$OUTROOT"
HOST_BIN="$OUTROOT/ssdd_reference_workload"
g++ -O2 -std=c++20 -static "$SOURCE" -o "$HOST_BIN"

case_names=()
case_modes=()
case_faults=()
case_records=()
add_case() { case_names+=("$1"); case_modes+=("$2"); case_faults+=("$3"); case_records+=("$4"); }

case "$CASE_SET" in
  limited)
    add_case cxl-asic-accepted cxl-asic none 18
    add_case cxl-asic-proof-corruption cxl-asic proof-corruption 18
    ;;
  full)
    add_case dram-control dram-control none 18
    add_case cxl-asic-accepted cxl-asic none 18
    add_case cxl-asic-proof-corruption cxl-asic proof-corruption 18
    add_case cxl-fpga-accepted cxl-fpga none 18
    add_case interleave-accepted interleave none 18
    ;;
  *)
    echo "unknown SSDD_SIMCXL_CASE_SET: $CASE_SET (use limited or full)" >&2
    exit 64
    ;;
esac

if [[ "$IN_PLACE_DISK" == "1" && "$CASE_SET" != "limited" ]]; then
  echo "setup-blocked: in-place disk staging is restricted to SSDD_SIMCXL_CASE_SET=limited" >&2
  exit 20
fi

printf 'case,memory_mode,fault,fault_record,guest_exit,validation,replay_digest,reference_digest,sim_exit\n' > "$OUTROOT/matrix.csv"
for index in "${!case_names[@]}"; do
  name="${case_names[$index]}"
  mode="${case_modes[$index]}"
  fault="${case_faults[$index]}"
  record="${case_records[$index]}"
  run_dir="$OUTROOT/$name"
  mkdir -p "$run_dir"
  if [[ "$IN_PLACE_DISK" == "1" ]]; then
    disk_copy="$SIMCXL_DISK"
    echo "warning: staging limited-case guest binary in-place; source-disk SHA-256 is retained in the run record" >&2
  else
    disk_copy="$run_dir/guest.img"
    cp --sparse=always --reflink=auto "$SIMCXL_DISK" "$disk_copy"
  fi
  staging_device="$disk_copy"
  loop_device=""
  if file "$disk_copy" | grep -q 'DOS/MBR boot sector'; then
    first_lba="$(od -An -t u4 -j 454 -N 4 "$disk_copy" | tr -d '[:space:]')"
    [[ "$first_lba" =~ ^[0-9]+$ && "$first_lba" -gt 0 ]] || {
      echo "setup-blocked: could not determine first MBR partition offset" >&2
      exit 20
    }
    loop_device="$(sudo losetup --find --show --offset "$((first_lba * 512))" "$disk_copy")"
    staging_device="$loop_device"
  fi
  sudo debugfs -w -R 'mkdir /home/ssdd' "$staging_device" >/dev/null 2>&1 || true
  sudo debugfs -w -R 'rm /home/ssdd/ssdd_reference_workload' "$staging_device" >/dev/null 2>&1 || true
  sudo debugfs -w -R "write $HOST_BIN /home/ssdd/ssdd_reference_workload" "$staging_device" >/dev/null
  sudo debugfs -w -R 'set_inode_field /home/ssdd/ssdd_reference_workload mode 0100755' "$staging_device" >/dev/null
  sudo debugfs -w -R 'rm /etc/systemd/system/multi-user.target.wants/ssdd-gem5-readfile.service' "$staging_device" >/dev/null 2>&1 || true
  sudo debugfs -w -R 'rm /etc/systemd/system/ssdd-gem5-readfile.service' "$staging_device" >/dev/null 2>&1 || true
  sudo debugfs -w -R "write $GUEST_SERVICE /etc/systemd/system/ssdd-gem5-readfile.service" "$staging_device" >/dev/null
  sudo debugfs -w -R 'symlink /etc/systemd/system/multi-user.target.wants/ssdd-gem5-readfile.service ../ssdd-gem5-readfile.service' "$staging_device" >/dev/null
  if [[ -n "$loop_device" ]]; then
    sudo losetup -d "$loop_device"
  fi

  set +e
  "$SIMCXL_BIN" -d "$run_dir/m5out" "$CONFIG" \
    --kernel="$SIMCXL_KERNEL" --disk-image="$disk_copy" --memory-mode="$mode" \
    --fault="$fault" --fault-record="$record" --boot-cpu="$BOOT_CPU" \
    > "$run_dir/simout" 2>&1
  sim_exit=$?
  set -e

  serial="$run_dir/m5out/board.pc.com_1.device"
  [[ -f "$serial" ]] || serial="$run_dir/simout"
  # The guest serial backend prefixes command output (for example, "sh[1072]: ").
  # Normalize only that transport prefix before selecting workload markers so the
  # retained summary and matrix reflect the actual guest result rather than blanks.
  sed -E 's/^[^:]+: //' "$serial" | tr -d '\r' | \
    grep -E '^(SSDD_REFERENCE_WORKLOAD|stages|replay_digest|reference_digest|memory_probe|fault_mode|fault_record|validation|SSDD_GUEST_EXIT=|SSDD_CXL_NUMA_)' \
    > "$run_dir/summary" || true
  guest_exit="$(awk -F= '/^SSDD_GUEST_EXIT=/{value=$2} END{print value+0}' "$run_dir/summary")"
  validation="$(awk -F= '/^validation=/{value=$2} END{print value}' "$run_dir/summary")"
  replay="$(awk -F= '/^replay_digest=/{value=$2} END{print value}' "$run_dir/summary")"
  reference="$(awk -F= '/^reference_digest=/{value=$2} END{print value}' "$run_dir/summary")"
  printf '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' "$name" "$mode" "$fault" "$record" "$guest_exit" "$validation" "$replay" "$reference" "$sim_exit" >> "$OUTROOT/matrix.csv"
  if [[ "$IN_PLACE_DISK" != "1" ]]; then
    rm -f "$disk_copy"
  fi
done

{
  printf 'simcxl_commit='; git -C "$SIMCXL_ROOT" rev-parse HEAD
  printf 'simcxl_binary_sha256='; sha256sum "$SIMCXL_BIN" | awk '{print $1}'
  printf 'kernel_sha256='; sha256sum "$SIMCXL_KERNEL" | awk '{print $1}'
  printf 'source_sha256='; sha256sum "$SOURCE" | awk '{print $1}'
  printf 'config_sha256='; sha256sum "$CONFIG" | awk '{print $1}'
  printf 'guest_binary_sha256='; sha256sum "$HOST_BIN" | awk '{print $1}'
  printf 'boot_cpu=%s\n' "$BOOT_CPU"
  printf 'case_set=%s\n' "$CASE_SET"
  printf 'disk_staging=%s\n' "$([[ "$IN_PLACE_DISK" == "1" ]] && echo in-place-limited || echo copied)"
} > "$OUTROOT/run-manifest.txt"
find "$OUTROOT" -type f \( -name 'summary' -o -name 'matrix.csv' -o -name 'run-manifest.txt' \) -print0 | sort -z | xargs -0 sha256sum > "$OUTROOT/SHA256SUMS"
echo "SimCXL Type-3 matrix completed. Local output: $OUTROOT"
