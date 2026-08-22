# SSDD Bare-Metal Execution Plan — 22 August 2026

**Status:** Prepared — awaiting explicit owner approval. No paid resource, booking, or hardware purchase has been made.

The owner-facing Arabic plan is retained separately for owner review. This repository record is self-contained: it preserves the operative, evidence-bounded decision, reproducibility pins, cost boundary, and evidence limits that govern the research validation set.

## Operative Decision

The proposed KVM path is a Cherry Servers **instant dedicated bare-metal** x86_64 host only—never a VPS and never nested KVM. Admission requires direct, readable/writable `/dev/kvm`, `vmx` or `svm` CPU flags, a successful gem5 KVM boot, an explicit switch to Timing CPU before the region of interest, retained `m5 resetstats`/`m5 dumpstats` boundaries, and raw artifacts. A host preflight alone is not performance evidence.[1] [2]

## Budget and Time Boundary

| Item | Value |
|---|---:|
| Campaign ceiling | 85 host-hours |
| Planning rate | US$0.40/hour |
| Exact host-time arithmetic | US$34.00 before tax, egress, or portal-specific extras |
| Published mid-tier reference range | US$17.00–US$51.00 for 85 hours at US$0.20–0.60/hour |
| Recommended owner-approved KVM spend ceiling | US$80 including contingency |
| Provisional smoke envelope | 8 hours / US$3.20 at the planning rate |

The published provider pricing is not a quote. Before any resource creation, the owner must approve the exact host, visible hourly price, currency, tax treatment, and the US$80 maximum. Any KVM gate failure results in immediate teardown; Atomic CPU is not a substitute for a performance branch.

## Work Schedule

| Window | Hours | Deliverable | Gate |
|---|---:|---|---|
| H0–H2 | 2 | Host facts, local/remote KVM preflight, hashes | `/dev/kvm` + `vmx`/`svm` mandatory |
| H2–H4 | 2 | Pinned SimCXL build and verified resources | Build compatible binary or stop |
| H4–H6 | 2 | gem5 KVM smoke and Timing CPU ROI smoke | KVM-to-Timing transition plus stats mandatory |
| H6–H8 | 2 | Admission record and decision | Stop/teardown on any smoke defect |
| H8–H25 | 17 | Matched baseline versus SSDD distributions | Cell-level manifests and raw stats |
| H25–H45 | 20 | 12-family adversarial falsification matrix | Explicit accepted/rejected/failed labels |
| H45–H60 | 15 | Full KVM-backed SimCXL matrix | Simulation-only scope retained |
| H60–H70 | 10 | Governance ablation where implementation permits | No invented fallback case |
| H70–H80 | 10 | Artifact packaging and SHA-256 verification | Complete manifests required |
| H80–H85 | 5 | Independent rerun, Git review/push, teardown | No extension after H85 |

## Reproducibility Pins

| Component | Source / commit |
|---|---|
| SSDD research | `uniqueteamyemen/ssdd-research` at `1717e0ea9119a8d68f16c15b67fde72b8c49019b` |
| SimCXL | `TianheMICALab/SimCXL` at `edddc2054bcdafdc7537b20c99605f2181bda9dc` |
| Simulator artifact | `build/X86/gem5.opt`, built on-host and SHA-256 recorded |
| Guest resources | CXL-aware kernel and guest disk transferred through an approved channel and SHA-256 recorded; not stored in Git |

The authoritative step-by-step operating guide, exact commands, preflight interpretation, owner prerequisites, and claim boundary are in the owner-facing plan above and the companion [`cloud-rental-kvm-runbook.md`](cloud-rental-kvm-runbook.md). The resulting claim remains: **“simulation-performance result under the recorded gem5/host configuration.”** It is not FPGA, physical CXL Type-3, silicon, or production evidence.

## References

[1]: [Cherry Servers — Dedicated Servers documentation](https://www.cherryservers.com/knowledge/docs/compute/dedicated-servers)
[2]: [gem5 — Using KVM CPUs](https://www.gem5.org/documentation/general_docs/using_kvm/)
[3]: [Cherry Servers — Bare-metal server cost](https://www.cherryservers.com/blog/bare-metal-server-cost)
[4]: [TianheMICALab — SimCXL](https://github.com/TianheMICALab/SimCXL)
