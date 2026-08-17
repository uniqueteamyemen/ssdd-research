# SSDD CXL-Aware Simulator Source Register

## Status

This is a working **source-discovery register**, created before simulator selection. An entry records a candidate and its primary source; it does not assert compatibility, correctness, performance, or suitability until the source and implementation are reviewed against SSDD’s retained reference workload.

| Candidate | Primary source | Discovery indication | Review status |
|---|---|---|---|
| SimCXL / CXL-DMSim | <https://github.com/TianheMICALab/SimCXL> | Full-system, cycle-level CXL simulation based on gem5; Type-3 CXL memory expander example | Candidate for executable evaluation: public source and documented build path |
| CXL-DMSim paper | <https://arxiv.org/html/2411.02282v6> | Full-system CXL disaggregated-memory model associated with SimCXL | Reviewed as the Type-3 model lineage; executable assessment uses the public SimCXL repository |
| CXLRAMSim | <https://arxiv.org/html/2603.29483v1> | gem5-integrated CXL memory-expander model positioned on the I/O bus | Architecture reviewed; no public implementation identified in the reviewed source, so not an executable first path |
| gem5 CXL project | <https://arch.cs.ucdavis.edu/projects/gem5-cxl> | CXL-oriented gem5 infrastructure research | Pending source review |
| CXLSim | <http://dicl.skku.edu/publications/CXLSim.pdf> | CXL memory-expander simulation research | Pending source review |

## Selection discipline

The selected path must preserve the existing SSDD deterministic inputs, manifests, acceptance structure, and evidence retention model. It must be reproducible from documented prerequisites and must support an explicit simulation-only interpretation boundary. It must not be represented as a real-CXL, silicon-timing, hardware-fault-tolerance, production-performance, security-certification, or production-readiness result.

## Reviewed findings

SimCXL documents a gem5 23.10-based full-system path for a Type-3 CXL memory expander, with CXL.io and CXL.mem support. Its documented Type-3 build emits `build/X86/gem5.opt`; its full-system flow requires a Linux kernel and disk image, then exposes the device as a CPU-less NUMA node that can be selected through `numactl` or its provided memory-management path. These properties make it a technically compatible next-stage candidate for an SSDD workload that already compiles to an x86 gem5 executable, but they also mean that the existing syscall-emulation harness cannot be reused unchanged. [1]

The CXL-DMSim study describes a full-system Type-3 memory-expander model with CXL.io and CXL.mem, a driver, and application-managed or NUMA-compatible kernel-managed memory modes. The paper’s own hardware calibration and accuracy results are evidence about the authors’ model evaluation, not SSDD evidence. SSDD will therefore retain the simulator revision and configuration for every run and treat any result only as a model-scoped simulation observation. [3]

CXLRAMSim describes a newer gem5-integrated design that places CXL devices on the I/O bus and uses an unmodified Linux 6.14 software stack. The reviewed paper reports a gem5 v25, Ubuntu 24.04-oriented environment and says that open-sourcing and gem5-mainline integration are planned. Because the reviewed source did not provide a runnable public implementation, it is retained as an architectural comparator rather than selected as the first reproducible execution path. [2]

The public SimCXL resource folder linked by the project currently exposes a `vmlinux` kernel artifact (36.3 MB) and a `parsec.img.xz` disk-image artifact (4.63 GB). The visible Google Drive identifiers are `16E2xIHcLEunZ-qFkOXj8J2CEJjHysxHI` for `vmlinux` and `1KWFbipRQOtobKsgR7ZzPweaCNWTWecmu` for `parsec.img.xz`. They are source prerequisites for the project’s documented full-system route; they have not yet been treated as an SSDD evidence input, and their checksums will be retained before any claimed test execution. [1]

## References

[1]: https://github.com/TianheMICALab/SimCXL "SimCXL repository and Type-3 setup"
[2]: https://arxiv.org/html/2603.29483v1 "CXLRAMSim v1.0 paper"
[3]: https://arxiv.org/html/2411.02282v6 "CXL-DMSim paper"
