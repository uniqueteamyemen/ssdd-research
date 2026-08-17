# SSDD CXL-Aware Simulation Decision Record

**Status:** Selected for staged setup; no SSDD CXL-aware result is claimed by this record.
**Decision date:** 2026-08-17
**Selected implementation revision:** SimCXL commit `edddc2054bcdafdc7537b20c99605f2181bda9dc`.

## Decision

SSDD’s next simulation stage will use the **SimCXL Type-3 CXL memory-expander path with the Classic memory system** as its initial executable target. SimCXL is a public, gem5 23.10-derived, full-system model that documents CXL.io and CXL.mem support for Type-3 memory expansion. The repository includes an x86 Type-3 configuration, and its project documentation identifies the CXL-DMSim implementation as integrated into that work. [1]

The existing SSDD controlled matrix is deliberately retained as a separate pre-hardware baseline. It uses syscall emulation, one reference CPU, and `SimpleMemory`; it is **not** a CXL model. The new path must not retroactively re-label any existing acceptance record as CXL-aware.

## Selection basis

| Candidate | Decision | Reason relevant to SSDD |
|---|---|---|
| SimCXL Type-3 / CXL-DMSim | **Selected for setup** | Public source, documented Type-3 configuration, gem5 lineage, and an OS-visible CXL-memory/NUMA workflow provide a reproducible route for the SSDD reference workload. [1] [2] |
| CXLRAMSim | Architectural comparator | The reviewed paper describes an I/O-bus-positioned CXL memory model and an unmodified Linux software stack, but the source reviewed for this decision does not supply a runnable public implementation. [3] |
| Existing SSDD gem5 SE harness | Retained as non-CXL control | It is intentionally model-scoped around `SimpleMemory`; retaining it unchanged preserves its established evidence boundary. |

> **Interpretation boundary.** An SSDD result from this path can establish only that the retained reference workload completed or was rejected under a named SimCXL configuration. It does not establish performance on a physical CXL device, silicon timing, platform compatibility, hardware fault tolerance, security certification, or production readiness.

## Required reproducibility inputs

SimCXL documents a full-system flow: an x86 simulator build, a compatible Linux kernel with the needed CXL support, and a disk image holding the workload. Its Type-3 example then boots the guest, enumerates the CXL memory as a NUMA node, and switches into a timing model to run the benchmark. [1]

| Input | Retention requirement | Rationale |
|---|---|---|
| SimCXL source | Remote URL, immutable commit, and local build log | Binds the model implementation used by a run. |
| Simulator binary | SHA-256 and build command | Binds the executable to the selected source. |
| Kernel and disk image | Provenance, release identifier, and SHA-256; do not commit image bytes to SSDD | Binds the full-system software environment without treating external image files as repository source. |
| SSDD guest workload | Source revision, static-binary SHA-256, and guest command | Binds deterministic input execution to the exact artifact. |
| CXL configuration | Repository-relative config revision and parameter manifest | Binds memory type, local/CXL capacity, CPU model, and management mode. |
| Results | Console output, gem5 statistics, workload summaries, hash manifest, and acceptance record | Allows independent review without a performance claim beyond the model. |

## Execution gates

The first run is permitted only after all of the following are checked: the selected SimCXL revision builds successfully; a kernel/disk pair of known provenance boots; the SSDD guest workload is present in the guest image; `numactl -H` visibly reports the expected CXL NUMA topology; and a baseline local-DRAM control is retained. If any prerequisite is unavailable, the output is a **setup-blocked record**, not a negative or positive SSDD result.

## Deferred decisions

This decision does not choose an RTL language, an RTL package, an FPGA board, or an FPGA timing target. Those choices remain gated on the future CXL-aware matrix producing retained, reproducible evidence and on a later interface-stability review. The first RTL/FPGA decision record will therefore consume the same archived workload and acceptance definitions rather than declaring a production path from simulation alone.

## References

[1]: https://github.com/TianheMICALab/SimCXL "SimCXL repository and Type-3 setup"
[2]: https://arxiv.org/html/2411.02282v6 "CXL-DMSim paper"
[3]: https://arxiv.org/html/2603.29483v1 "CXLRAMSim v1.0 paper"
