# SSDD Cherry Timing Evidence and Chiplet Summit 2027 Readiness

**Purpose:** Final table for submission preparation.  
**Evidence rule:** A number appears below only if it exists in a retained artifact and can be traced to its declared execution domain. The table does not merge the KVM-to-Timing SimCXL matrix with the separate native-reference scale/load exercise.

## 1. What Cherry established about KVM, SimCXL, timing, and jitter

| Evidence domain | CPU / execution path | What was actually observed | Timing or latency quantity available | Jitter / p95 / p99 available? | Submission-safe conclusion |
|---|---|---|---|---|---|
| **Full-system SimCXL matrix** | `boot_cpu=kvm` → switch to Timing CPU → guest-delimited ROI | Five declared memory/fault cells; three independently retained ROI-closed executions reproduced expected acceptance/rejection semantics | No normalized timing metric. Nonzero Timing-CPU `numCycles` proves that Timing CPU executed after the switch, not a speed comparison. | **No.** No per-epoch samples, distribution, or percentile artifact. | Cherry establishes a KVM-to-Timing full-system SimCXL **behavioral path**, not latency or jitter performance. |
| **SimCXL `cxl-asic`, `cxl-fpga`, and interleave modes** | Variants inside the full-system SimCXL behavioral matrix | Accepted/rejected semantic outcomes at the stated simulation scope | No per-mode timing-difference result retained. | **No.** | The labels identify **simulator modes**, not physical CXL or FPGA devices; no KVM-versus-CXL speed comparison is supported. |
| **Controlled gem5 matrix** | Syscall-emulation; `BaseTimingSimpleCPU` | Model-specific timing-sensitivity and fault configurations | No closed baseline-versus-SSDD or CXL-versus-KVM timing comparison. | **No.** | Confirms TimingSimpleCPU in a separate controlled model domain; it is not KVM evidence. |
| **SCL-01 native-reference scale** | `native_reference_wallclock`; 8 → 128 logical nodes | Stored mean internal components and `epoch_success_rate = 1.0` at every point | `T_total`: **12.152 → 177.625 µs**, Δ **+165.473 µs** (+1361.694%). `T_ssc`: **9.143 → 147.336 µs**, Δ **+138.193 µs**. | **No.** Per-point means only. | These are reference-model mean internal timings under a 16× modeled scale change, not CXL, KVM, fabric, or device latency. |
| **LOD-01 native-reference load** | `native_reference_wallclock`; 1,000 → 100,000 events/s-equivalent | Stored mean internal components and `epoch_success_rate = 1.0` at every point | `T_total`: **1.274 → 33.085 µs**, Δ **+31.811 µs** (+2496.939%). `T_ssc`: **0.520 → 26.605 µs**, Δ **+26.085 µs**. | **No.** Per-point means only. | These are reference-model mean internal timings under a 100× modeled input change, not measured end-to-end latency or throughput. |

### Direct answer on “KVM versus CXL” latency and jitter

There is **no retained direct numerical comparison** of KVM versus CXL latency, nor a retained CXL jitter distribution. The KVM-to-Timing SimCXL matrix proves the execution path and behavioral results. The SCL-01/LOD-01 JSON proves separately derived mean internal timings in the `native_reference_wallclock` domain. Comparing their numbers as if they were one benchmark would be scientifically invalid because their CPU modes, execution domains, and metric contracts differ.[^reconcile] [^claim] [^timing]

> **Use in the submission:** “The corpus includes KVM-to-Timing full-system SimCXL behavioral evidence and separately retained reference-model mean internal timing records. It does not report direct KVM-versus-CXL latency, jitter, percentile, throughput, or baseline-improvement results.”

## 2. Final Chiplet Summit 2027 file and field readiness matrix

| File or form field | State | Where it is ready now | What remains before a human submits |
|---|---|---|---|
| Presentation title | **Ready** | `chiplet-summit-2027-form-packet.md` | Confirm against any 2027 field-length rule. |
| Abstract variants A/B/C | **Ready** | `chiplet-summit-2027-abstract-variants.md` | Select the longest variant that fits the live 2027 counter. |
| Default abstract | **Ready** | Variant B: 1,338 characters / 165 words | Confirm live character accounting before paste. |
| Scientific claim-boundary statement | **Ready** | `cherry-measurement-claim-matrix-20260823.md` | Keep unchanged in abstract, slides, and notes. |
| KVM-to-Timing execution record | **Ready** | `cherry-kvm-full-matrix-evidence-20260822.md` and reconciliation note | Link only if a supplementary-material field is available. |
| SCL-01 / LOD-01 timing-difference report | **Ready** | `cherry-scl-lod-derived-timing-differences-20260823.md` | Describe only as native-reference mean internal timing. |
| Derived machine-readable timing table | **Ready** | `cherry-scl-lod-timing-deltas-20260823.json` | Retain for audit; attach only if requested. |
| Reproducible derivation tool | **Ready** | `tools/derive-scl-lod-timing-deltas.mjs` | Retain for audit; attach only if requested. |
| Nine-ID evidence index | **Ready** | `cherry-nine-test-campaign-evidence-index-20260822.md` | Link only if permitted by the form. |
| Requirements-status record | **Ready** | `chiplet-summit-2027-requirements-status.md` | Recheck after the official form appears. |
| Presenter biography | **Draft ready** | `chiplet-summit-2027-form-packet.md` | Owner confirms final wording. |
| Presenter name, affiliation, contact details | **Partially ready** | Form packet includes proposed name/affiliation | Owner enters/approves final spelling, email, phone, and any required profile data. |
| Topic category | **Recommended, not final** | Form packet recommends Technology Areas / HPC | Select only from the live 2027 category list. |
| 2027 abstract limit and deadline | **Not published on call page** | Official status record | Copy from the live official form when it appears. |
| Copyright/privacy consent | **Pending** | No 2027 text available | Owner reads and accepts/rejects the live form text. |
| Speaker slides | **Not started deliberately** | None | Build against the 2027 speaker template once supplied; do not use a historical template as final format. |
| Final form submission | **Not started** | N/A | Requires live form, owner fields, live consent, and explicit owner confirmation. |

## 3. Immediate action when the call opens

1. Open the official 2027 Call for Presentations page and record the deadline, categories, limits, and consent text.
2. Select the appropriate abstract variant by the form’s **actual** character counter.
3. Confirm the presenter biography, affiliation, contact information, and category with the owner.
4. Recheck every quantitative phrase against the claim matrix.
5. Add evidence links only if the form permits supplementary material.
6. Submit only after explicit owner approval.

## Evidence references

[^reconcile]: [`cherry-execution-mode-reconciliation-20260823.md`](../validation/cherry-execution-mode-reconciliation-20260823.md)
[^claim]: [`cherry-measurement-claim-matrix-20260823.md`](../validation/cherry-measurement-claim-matrix-20260823.md)
[^timing]: [`cherry-scl-lod-derived-timing-differences-20260823.md`](../validation/cherry-scl-lod-derived-timing-differences-20260823.md)
