# SSDD Pre-Hardware Verification Source Catalog

## Purpose

This catalog records the local source materials used to define the next SSDD verification program. It distinguishes **design intent and proposed acceptance criteria** from measurements that have actually been reproduced in the current gem5 pathway.

| Source record | Local source | Relevant design material | Evidence boundary |
|---|---|---|---|
| SSDD engine reference | `/home/ubuntu/upload/ssdd_engine.pycode.py` | Quadruple-key packet ordering; sidecar batching; Q32.32 aggregation and fusion; SHA-256 ledger serialization; deterministic RNG. | The file imports `q32_32_core`, which is not present beside it. The new harness must implement and test the specified behavior independently rather than claim execution of the incomplete package. |
| SSDD specification v1.2 | `/home/ubuntu/upload/pasted_file_xbcJOF_SSDD_Specification_V1.2_FINAL-17MAR26.pdf` | SSC ordering, epoch state evolution, Q32.32 state-critical arithmetic, and ledger-oriented determinism. | Design and acceptance source; not hardware validation. |
| SSDD implementation manual v1.2 | `/home/ubuntu/upload/pasted_file_uD1YHX_SSDD_Implementation_Manual_V1.2_FINAL-17MAR26.pdf` | Saturating arithmetic and deterministic ledger recomputation expectations. | Defines implementation intent; every asserted outcome must be tied to a retained test artifact. |
| SSDD prototype roadmap v1.2 | `/home/ubuntu/upload/pasted_file_7l4xNF_SSDD_Prototype_Roadmap_V1.2_FINA-17MAR26.pdf` | Packet-drop, node-delay, aggregator-failure, cross-language, scaling, and throughput objectives. | Roadmap objectives are not reported as completed results until reproduced. |
| Bounded-domain paper variants | `/home/ubuntu/upload/pasted_file_OXqrHy_ديبسيكمعالتعديلات.txt`, `/home/ubuntu/upload/pasted_file_PyryQB_لاتكسasplos26.txt` | Four-key SSC definition; bounded-domain language; ledger and Q32.32 rationale. | The variants contain proposed or simulator-reported figures that are not imported into the public site or gem5 evidence without independent reproduction. |

No `*.rs` source file or `Cargo.toml` manifest was present in the currently uploaded source paths when this catalog was prepared. The cross-language check will therefore use a small, retained Rust reference implementation that reproduces the documented canonical byte serialization and SHA-256 ledger rule; it will not be described as verification against an externally supplied production Rust implementation.

## Current Test Scope

The pre-hardware suite will test a software reference model and selected syscall-emulation executions through gem5. It will not claim validation of physical timing, CXL traffic, silicon behavior, million-node performance, security certification, or production readiness.

## Required Evidence Rules

Every completed experiment must preserve its input seed, serialized workload or generation rule, command line, implementation version, per-epoch hash chain or result manifest, and a statement of the model boundary. A failed acceptance case must be preserved as a result, not silently discarded.
