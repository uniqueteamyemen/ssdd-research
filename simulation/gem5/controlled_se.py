"""Controlled SSDD syscall-emulation configuration for model-scoped gem5 tests.

This file stays intentionally close to gem5's deprecated ``se.py`` example,
but it fixes the reference workload to one process and exposes only a
SimpleMemory latency switch for the experiment matrix. It is not a CXL model
or a hardware-validation configuration.
"""

import argparse
import os
import sys
from pathlib import Path

import m5
from m5.objects import AddrRange, Process, Root, SEWorkload, SrcClockDomain, System, SystemXBar, VoltageDomain
from m5.util import addToPath, fatal

from gem5.isas import ISA

GEM5_ROOT = Path(os.environ.get("GEM5_ROOT", "")).expanduser()
if not GEM5_ROOT.is_dir():
    fatal("controlled_se.py requires GEM5_ROOT to name a compatible gem5 checkout")
CONFIG_ROOT = GEM5_ROOT / "configs"
if not CONFIG_ROOT.is_dir():
    fatal(f"Missing gem5 configuration directory: {CONFIG_ROOT}")
addToPath(str(CONFIG_ROOT))

from common import CacheConfig, CpuConfig, MemConfig, ObjectList, Options, Simulation  # noqa: E402

parser = argparse.ArgumentParser(description="Controlled SSDD gem5 SE experiment")
Options.addCommonOptions(parser)
Options.addSEOptions(parser)
parser.add_argument(
    "--ssdd-memory-latency",
    required=True,
    help="Latency assigned to SimpleMemory for this model-scoped run, for example 10ns.",
)
args = parser.parse_args()

if not args.cmd:
    fatal("A workload command is required")
if args.mem_type != "SimpleMemory":
    fatal("controlled_se.py requires --mem-type=SimpleMemory")
if args.num_cpus != 1:
    fatal("controlled_se.py supports one reference CPU")

process = Process(pid=100)
process.executable = args.cmd
process.cwd = os.getcwd()
process.gid = os.getgid()
process.cmd = [args.cmd] + (args.options.split() if args.options else [])

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(args)
CPUClass.numThreads = 1
system = System(
    cpu=[CPUClass(cpu_id=0)],
    mem_mode=test_mem_mode,
    mem_ranges=[AddrRange(args.mem_size)],
    cache_line_size=args.cacheline_size,
)
system.voltage_domain = VoltageDomain(voltage=args.sys_voltage)
system.clk_domain = SrcClockDomain(clock=args.sys_clock, voltage_domain=system.voltage_domain)
system.cpu_voltage_domain = VoltageDomain()
system.cpu_clk_domain = SrcClockDomain(clock=args.cpu_clock, voltage_domain=system.cpu_voltage_domain)
system.cpu[0].clk_domain = system.cpu_clk_domain

if args.elastic_trace_en:
    CpuConfig.config_etrace(CPUClass, system.cpu, args)
if ObjectList.is_kvm_cpu(CPUClass) and ISA.X86 == ObjectList.cpu_list.get_isa(args.cpu_type):
    system.kvm_vm = m5.objects.KvmVM()

system.cpu[0].workload = process
system.cpu[0].createThreads()
system.membus = SystemXBar()
system.system_port = system.membus.cpu_side_ports
CacheConfig.config_cache(args, system)
MemConfig.config_mem(args, system)

for controller in system.mem_ctrls:
    controller.latency = args.ssdd_memory_latency

system.workload = SEWorkload.init_compatible(args.cmd)
root = Root(full_system=False, system=system)
Simulation.run(args, root, system, FutureClass)
