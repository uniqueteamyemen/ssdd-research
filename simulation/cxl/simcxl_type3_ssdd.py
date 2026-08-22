"""SSDD full-system SimCXL Type-3 configuration.

This configuration is a model-scoped simulation adapter. It reuses the
deterministic SSDD reference workload, but it does not turn any result into a
hardware, silicon, or production claim.
"""

import argparse

import m5
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_shared_l3_cache_hierarchy import (
    PrivateL1PrivateL2SharedL3CacheHierarchy,
)
from gem5.components.memory.single_channel import DIMM_DDR5_4400, SingleChannelDDR4_3200
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.isas import ISA
from gem5.resources.resource import DiskImageResource, KernelResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires


requires(isa_required=ISA.X86)

parser = argparse.ArgumentParser(description="SSDD SimCXL Type-3 full-system validation")
parser.add_argument("--kernel", required=True, help="Path to a compatible CXL-aware kernel")
parser.add_argument("--disk-image", required=True, help="Path to a mutable copy of a compatible guest disk image")
parser.add_argument(
    "--memory-mode",
    choices=("dram-control", "cxl-asic", "cxl-fpga", "interleave"),
    required=True,
    help="Guest allocation policy applied to the fixed SSDD workload.",
)
parser.add_argument("--fault", choices=("none", "proof-corruption"), required=True)
parser.add_argument("--fault-record", type=int, default=18)
parser.add_argument("--boot-cpu", choices=("kvm", "atomic"), required=True)
parser.add_argument("--guest-binary", default="/home/ssdd/ssdd_reference_workload")
args = parser.parse_args()

if args.fault == "proof-corruption" and not 1 <= args.fault_record <= 35:
    parser.error("--fault-record must be within 1..35 for the fixed SSDD reference workload")

cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
    l1d_size="48kB",
    l1d_assoc=6,
    l1i_size="32kB",
    l1i_assoc=8,
    l2_size="2MB",
    l2_assoc=16,
    l3_size="96MB",
    l3_assoc=48,
)

local_memory = DIMM_DDR5_4400(size="3GB")
cxl_memory = DIMM_DDR5_4400(size="8GB")
is_asic = args.memory_mode != "cxl-fpga"
if not is_asic:
    cxl_memory = SingleChannelDDR4_3200(size="8GB")

boot_cpu = CPUTypes.KVM if args.boot_cpu == "kvm" else CPUTypes.ATOMIC
processor = SimpleSwitchableProcessor(
    starting_core_type=boot_cpu,
    switch_core_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = X86Board(
    clk_freq="2.4GHz",
    processor=processor,
    memory=local_memory,
    cache_hierarchy=cache_hierarchy,
    cxl_memory=cxl_memory,
    is_asic=is_asic,
)

memory_policy = {
    "dram-control": "--cpunodebind=0 --membind=0",
    "cxl-asic": "--cpunodebind=0 --membind=1",
    "cxl-fpga": "--cpunodebind=0 --membind=1",
    "interleave": "--cpunodebind=0 --interleave=0,1",
}[args.memory_mode]
workload_args = f"--fault={args.fault} --fault-record={args.fault_record}"
command = (
    "m5 exit; "
    "echo SSDD_CXL_NUMA_BEGIN; numactl -H; echo SSDD_CXL_NUMA_END; "
    "echo SSDD_TIMING_CPU_ROI_BEGIN; "
    "m5 resetstats; "
    f"numactl {memory_policy} {args.guest_binary} {workload_args}; "
    "status=$?; echo SSDD_GUEST_EXIT=$status; "
    "m5 dumpstats; echo SSDD_TIMING_CPU_ROI_END; m5 exit"
)

board.set_kernel_disk_workload(
    kernel=KernelResource(local_path=args.kernel),
    disk_image=DiskImageResource(local_path=args.disk_image),
    readfile_contents=command,
    kernel_args=board.get_default_kernel_args() + ["idle=nomwait"],
)

simulator = Simulator(
    board=board,
    on_exit_event={ExitEvent.EXIT: (func() for func in [processor.switch])},
)

print("SSDD_SIMCXL_TYPE3_CONFIG v0.1")
print(f"memory_mode={args.memory_mode}")
print(f"fault={args.fault}")
print(f"fault_record={args.fault_record if args.fault == 'proof-corruption' else 0}")
print(f"boot_cpu={args.boot_cpu}")
print("roi_cpu=timing-after-first-exit-event")
simulator.run()
