# Chiplet Summit 2027 — Abstract Draft

**Status:** Draft for the official Call for Presentations form.  
**Recommended 2026-style category:** Technology Areas / High-Performance Computing (HPC), subject to the category list in the 2027 form.  
**Working title:** **SSDD: Pre-Silicon Quantitative Behavioral Characterization of Distributed Memory-System Execution**

## Draft abstract

Distributed memory-system execution can fail at the boundary between local handling and the shared meaning of an event. This work presents SSDD, a pre-silicon systems-design study of shared containment and reference treatment for distributed memory-system execution. The evaluation is intentionally separated into bounded execution domains.

The retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix. The guest booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, five declared memory/fault cells reproduced their expected semantic outcomes: DRAM control, accepted CXL-ASIC simulator mode, proof-corruption rejection, accepted CXL-FPGA simulator mode, and accepted interleave mode. The `cxl-asic` and `cxl-fpga` labels denote simulator modes, not physical devices.

A separate syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments. A retained native-reference scale/load exercise recorded mean internal timing components across 8–128 logical nodes and 1,000–100,000 input events/s-equivalent. For example, stored reference-model mean `T_total` changes from 12.152 µs to 177.625 µs across the node endpoints and from 1.274 µs to 33.085 µs across the input endpoints. These values describe the stated reference model only.

The contribution is a reproducible, evidence-bounded characterization method: preserve the execution path, simulation mode, guest ROI markers, semantic acceptance/rejection, configurations, manifests, and integrity checks; then keep model timing separate from device or fabric performance. We report neither physical-CXL or FPGA behavior nor latency, jitter, percentile, throughput, baseline-versus-SSDD, or production claims. The result is a pre-silicon basis for later controlled quantitative comparisons rather than a replacement for them.

## Mandatory claim boundary to keep with the abstract

This submission describes simulation and reference-model evidence. It does not claim physical CXL Type-3 validation, FPGA implementation, hardware latency, jitter, p95/p99, network throughput, or performance improvement over a baseline.

## Evidence basis

- [`../validation/cherry-kvm-full-matrix-evidence-20260822.md`](../validation/cherry-kvm-full-matrix-evidence-20260822.md)
- [`../validation/cherry-scl-lod-derived-timing-differences-20260823.md`](../validation/cherry-scl-lod-derived-timing-differences-20260823.md)
- [`../validation/cherry-measurement-claim-matrix-20260823.md`](../validation/cherry-measurement-claim-matrix-20260823.md)
