# Chiplet Summit 2027 — SSDD Owner-Review Package

**Status:** Final review copy. It is ready for owner review and live-form completion; it is **not submitted**.  
**Submission rule:** Do not submit until the 2027 form’s deadline, title/abstract limits, category list, supplementary-material rules, and consent text are visible and reviewed by the owner.

## 1. Decision statement

> **What is established now:** SSDD’s declared semantic-commit containment mechanism was exercised in three separate retained domains: a native reference harness, controlled syscall-emulation gem5, and full-system KVM-to-Timing SimCXL/gem5 behavioral simulation. Under the declared variations, it preserved the canonical accepted result or rejected/contained the invalid candidate before a normal new commit.[1] [2] [3]

> **What remains a future test:** Whether SSDD is simpler, clearer, lower-overhead, or otherwise preferable to a serious CAS/retry or single-writer-sequencer alternative. That is a separate controlled comparison; it is not a missing prerequisite for the completed mechanism evidence.[4]

The package must not claim physical CXL Type-3 behavior, FPGA behavior, silicon behavior, CXL-versus-KVM latency, jitter, p95/p99, throughput, scaling performance, baseline improvement, or production performance.[5]

## 2. Copy-ready form material

| Field | Review-copy value | Live-form control |
|---|---|---|
| Presentation title | **SSDD: Pre-Silicon Quantitative Behavioral Characterization of Distributed Memory-System Execution** | Confirm any field-specific title limit. |
| Presenter | **Abobakr Ahmed Awadh** | Owner confirms exact spelling. |
| Role | **Owner & Chief Executive Officer** | Use only if requested. |
| Affiliation | **Deterministic Solutions and Design** | Use the live form’s required organization format. |
| Legal entity, if requested | **Deterministic Solutions and Design LLC** | Use only if specifically requested. |
| Recommended topic | **Technology Areas / High-Performance Computing (HPC)** | Select only if a matching official 2027 category exists. |
| Keywords, if requested | `chiplets; distributed memory systems; SimCXL; gem5; KVM-to-Timing CPU; behavioral validation; systems design; traceability` | Do not add a keyword field if the form lacks one. |
| Additional presenter | **None proposed** | Change only with owner approval. |
| Contact email and telephone | **Owner enters in the live form** | Do not store or publish private contact data in this package. |

### Presenter biography

> Abobakr Ahmed Awadh is the Owner and Chief Executive Officer of Deterministic Solutions and Design, a New Mexico systems-design and research office. His work focuses on making consequential execution details visible and developing bounded, evidence-led methods for shared system behavior. He leads the SSDD pre-silicon research direction and its documented validation record.

Use this text only after the owner confirms it and only within the limit shown by the live form. It makes no academic-credential, hardware-performance, or production-deployment claim.

## 3. Recommended abstract and size alternatives

**Recommended default: Variant B — 1,338 characters / 165 words.** Use it only if the live 2027 form admits it. If the form is shorter, use Variant A; use Variant C only if its exact counter permits it. The historical 2026 limit is not a 2027 rule.[6]

### Variant A — 681 characters / 84 words

SSDD is a pre-silicon study of shared containment and reference treatment for distributed memory-system execution. Its retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix that booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Three independently retained ROI-closed executions reproduced expected acceptance or rejection semantics across five declared memory/fault cells. Separate TimingSimpleCPU and native-reference exercises retain model-specific timing means and integrity evidence. The work reports bounded simulation behavior, not physical-CXL, FPGA, latency, jitter, throughput, or production claims.

### Variant B — 1,338 characters / 165 words

Distributed memory-system execution can fail at the boundary between local handling and the shared meaning of an event. SSDD is a pre-silicon systems-design study of shared containment and reference treatment for that boundary. The retained corpus separates its execution domains. A Cherry-hosted full-system SimCXL/gem5 matrix booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, five declared memory/fault cells reproduced their intended acceptance or rejection semantics: DRAM control, two accepted CXL simulator modes, an accepted interleave mode, and a proof-corruption rejection. A separate syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments. Native-reference scale/load records retain mean internal timing components across 8–128 logical nodes and 1,000–100,000 input events/s-equivalent. The contribution is an evidence-bounded characterization method that preserves configuration, simulation mode, ROI markers, semantic outcomes, and integrity records while keeping model timing separate from hardware or fabric performance. The work makes no physical-CXL, FPGA, latency, jitter, percentile, throughput, baseline-comparison, or production claim.

### Variant C — 1,952 characters / 249 words

Distributed memory-system execution must preserve a shared interpretation of an event even when local processing paths and memory placements differ. SSDD is a pre-silicon systems-design study of shared containment and reference treatment for this problem. Its evaluation is organized as bounded evidence domains rather than one undifferentiated performance claim.

The retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix. The guest booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, the five declared memory/fault cells reproduced their expected semantic outcomes: DRAM control, accepted CXL-ASIC simulator mode, proof-corruption rejection, accepted CXL-FPGA simulator mode, and accepted interleave mode. The CXL labels denote simulator modes, not physical devices. A separate syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments.

The retained native-reference scale/load exercise records mean internal timing components over 8–128 logical nodes and 1,000–100,000 input events/s-equivalent. Its stored mean `T_total` changes from 12.152 µs to 177.625 µs across the node endpoints and from 1.274 µs to 33.085 µs across the input endpoints. These are reference-model means, not device or fabric latency measurements. The retained bundle contains no per-epoch timing distribution and therefore supports neither jitter nor percentile claims.

The contribution is a reproducible, evidence-bounded characterization method: preserve the execution path, configuration, guest ROI markers, semantic acceptance/rejection, source hashes, manifests, and integrity checks; then keep reference-model timing distinct from hardware performance. The result is a pre-silicon basis for later controlled quantitative comparisons, not a replacement for them.

## 4. Final documentation of the completed gem5 evidence

The controlled gem5 matrix is a **separate syscall-emulation model domain**. It used one process, `TimingSimpleCPU`, `SimpleMemory`, and declared model-latency inputs. It is not KVM, Type-3 CXL, FPGA, physical hardware, or a baseline-versus-SSDD performance experiment.[2]

| Required final record | Retained result | Submission-safe use |
|---|---|---|
| Execution identity | 21 completed runs; runner exit status `0`; pinned SimCXL commit, SSDD source commit, binary/runner/workload/configuration SHA-256 values retained. | Establishes reproducibility provenance for this domain. |
| Latency-input sensitivity | 10 ns, 50 ns, and 100 ns model inputs produced distinct `sim_ticks` while retaining the same accepted replay/reference/probe digest tuple. | “The tested accepted semantic result was invariant under these declared model-latency inputs.” |
| Fixed-input replay | Five 50 ns replays retained the same accepted digest trio and the same retained tick total. | “The fixed model/workload replayed deterministically in the retained set.” |
| Proof mutation | Selected mutations at records 1, 18, and 35 were rejected as designed. | “The selected corrupted candidates were rejected by the tested validator path.” |
| Artifact trail | Matrix CSV, manifest, configuration, `simout`, `summary`, `sim_ticks`, `stats.txt`, remote/local checksum checks, and inventory retained. | Provide only as permitted supplementary evidence. |

### Mandatory gem5 wording control

Use **“model-specific timing sensitivity”**, never “latency improvement,” “jitter reduction,” “CXL latency,” “hardware performance,” or “throughput.” The retained ticks are not wall-clock latency, p95/p99, jitter, CPU overhead, memory overhead, or a physical-memory measure.[2] [5]

## 5. Final documentation of the completed SimCXL evidence

The full-system SimCXL/gem5 matrix is a **KVM boot → Timing CPU switch → guest-delimited ROI behavioral simulation**. It is distinct from the controlled gem5 domain. The labels `cxl-asic` and `cxl-fpga` identify simulator modes, not physical devices.[3]

| Required final record | Retained result | Submission-safe use |
|---|---|---|
| Execution path | `boot_cpu=kvm`; switch to Timing CPU before ROI; every cell retained CPU-switch and ROI markers. | “The full-system behavioral path was exercised under KVM and Timing CPU inside the declared ROI.” |
| Five declared cells | `dram-control` accepted; `cxl-asic` accepted; `cxl-asic` proof corruption rejected; `cxl-fpga` accepted; `interleave` accepted. | “The declared simulator-mode/fault cells produced the intended acceptance or rejection semantics.” |
| Semantic criterion | Accepted rows retained replay/reference digest `ff05ec2371488ba1`; the proof-corruption candidate had a distinct replay digest and was rejected. | “The accepted semantic outcome was preserved for the declared accepted rows; the selected corrupted candidate was rejected.” |
| Behavioral repetition | Runs 1, 2, and 4 are independently retained ROI-closed executions with identical five-row semantic matrices; run 3 is retained as a semantic replicate with a documented missing ROI-close marker in one rejection cell. | “Three ROI-closed behavioral executions were retained.” Do not count run 3 as ROI-closed. |
| Integrity/provenance | Pinned commits, clean worktree state, binary/kernel/config/workload hashes, copied-disk safeguard, manifests, logs, stats, and remote/local SHA-256 checks retained. | Enables an audit trail; attach only if allowed. |

### Mandatory SimCXL wording control

Use **“full-system SimCXL/gem5 behavioral matrix”**, **“KVM-to-Timing execution path”**, and **“simulator mode.”** Do not describe it as physical CXL Type-3, FPGA evidence, silicon behavior, a benchmark, a CXL-versus-DRAM comparison, or a latency/jitter/throughput/scaling/overhead result.[3] [5]

## 6. Measurement ledger for the review package

| Quantity | Present in retained evidence? | Allowed wording | Prohibited inference |
|---|---|---|---|
| KVM-to-Timing CPU transition | Yes | Full-system behavioral execution path; ROI markers and nonzero Timing-CPU work were retained. | KVM performance, timing speedup, or latency. |
| `sim_ticks` under 10/50/100 ns model inputs | Yes | Model-specific timing-sensitivity result in a fixed syscall-emulation gem5 workload. | Wall-clock latency, jitter, p95/p99, throughput, or hardware/CXL behavior. |
| Native-reference mean timing values | Yes | Mean internal reference-model components at stated scale/load endpoints. | Device/fabric latency, end-to-end throughput, jitter, or comparison to SimCXL. |
| Jitter, p95, p99, distributions | No | State explicitly that no retained distribution supports these metrics. | Any numerical jitter or percentile statement. |
| SSDD-versus-baseline outcome | No | State that comparative evidence is planned, not executed. | Simpler, faster, superior, or lower-overhead claim. |

## 7. Fair SSDD-versus-conventional comparison protocol

### Current local comparative status

The first local policy-reference gates have now been completed under one 133-case contract: one positive control, 128 arrival permutations, exact conflicting identity, late-source/incomplete set, proof corruption, and candidate-state corruption. SSDD, the CAS/retry reference, and the single-writer-sequencer reference each produced 129 accepted, 3 rejected, and 1 deferred disposition, with one accepted referee checkpoint digest across the 128 arrival permutations. This **does not establish a winner**. The serious baselines explicitly added canonical candidate/queue-drain policies and matched the bounded semantic contract.[8]

The honest current conclusion is therefore: **SSDD is not needed merely to obtain the tested semantics; a serious CAS/retry or sequencer alternative can match them in this bounded local scenario.** The remaining value question is whether one policy gives the engineer a materially clearer, more inspectable decision/evidence path under the same review task. That is pending the predeclared blinded reviewer and policy-surface review.[9]

### Purpose and fair question

The future campaign must not ask whether conventional CXL systems are coherent or whether a weak baseline can be made to fail. It asks one narrower question:

> **For the same shared-checkpoint task, inputs, faults, and execution domain, does SSDD provide a more contained, semantically invariant, diagnostically clear, or policy-compact implementation than credible alternatives?**

The comparison begins only after all three arms and all expected dispositions are predeclared. A sequencer that matches or exceeds SSDD defeats any general simplicity/superiority statement.[4]

### Three implementation arms

| Arm | Honest implementation contract | Why it is required |
|---|---|---|
| A. Arrival-order CAS/retry | Shared-memory CAS/retry with idempotency keys, arrival-order application, and explicit retry/timeout policy. | Represents a credible optimistic shared-memory alternative. |
| B. Single-writer sequencer | Explicit queue/sequencer that chooses order and publishes checkpoints, including declared failover/retry/proof treatment. | Prevents claiming value merely by comparing SSDD to a weak unordered baseline. |
| C. SSDD policy | Four-field canonical key; exact-collision rejection; canonical batch; declared reduction; state/hash chain; validation before commit; declared reject/defer behavior. | Tests SSDD’s actual mechanism under the same contract. |

### Fixed contract before the first run

Every arm must receive the same versioned manifest, event payloads, key definitions, producer schedule, seed, initial state, fault schedule, expected-disposition table, and repeat count. Record the execution domain independently: native multi-process software, controlled syscall-emulation gem5, or full-system KVM-to-Timing SimCXL. Never transfer a result from one domain to another.[4]

| Case family | Fixed injection | Required retained observation |
|---|---|---|
| Positive control | One complete admitted event set | Final checkpoint/state digest and disposition. |
| Arrival permutations | 128 shuffles plus a separate longer-chain set | Equality only where the arm’s contract requires it; otherwise the named differing disposition. |
| Exact key collision | Same ordering fields with changed payload/source field | Explicit reject, resolve, or other predeclared outcome. |
| Late source | Producer crossing an epoch/commit boundary | Explicit accept/reject/defer/retry and state effect. |
| Proof corruption | Selected proof-field or record mutation | Pre-commit rejection/containment or the baseline’s documented treatment. |
| State corruption | Candidate checkpoint changed before publication | Containment result and identification of the prior valid checkpoint. |
| Mode variation | Declared DRAM-control, CXL-aware simulator, interleave, and model-latency points | Semantic result separately from any predeclared performance metric. |
| Independent replay | Rerun from the same manifest | Reproducibility evidence within the arm’s declared contract. |

### How the engineer-facing effect is measured fairly

| Value dimension | Evidence to retain | SSDD claim allowed only if supported |
|---|---|---|
| Containment | Corrupted/incomplete candidate cannot produce an undocumented new checkpoint; prior valid checkpoint remains identifiable. | It contained the tested failures under its declared policy. |
| Semantic invariance | Same admitted set produces the required same result or named disposition under declared variation. | It separated tested semantic outcome from the declared path variation. |
| Diagnostic clarity | Reviewer traces manifest → order/decision record → checkpoint/hash → disposition without reconstructing unrelated logs. | Its retained evidence path was clearer for this scenario. |
| Policy compactness | Predeclared count and description of independent ordering, retry, integrity, and commit rules per arm. | This implementation used fewer or more unified policy surfaces—not that all systems will. |
| Performance cost | Separate, preregistered KVM-to-Timing matrix with identical workload, warm-up, ROI, repetitions, raw timing/counter files, and planned statistics. | Only the measured overhead/latency result, with its exact scope. |

### Mandatory fairness and falsification rules

The baseline source must be serious, documented, and capable of passing; an intentionally weak baseline invalidates the campaign. SSDD’s value statement must be narrowed or withdrawn if it breaks a required invariant, normal-commits a corrupted/incomplete candidate, or a baseline matches the containment and diagnostic criteria with an equal or smaller policy surface. A result that mixes native, syscall-emulation, KVM-to-Timing, or physical-domain claims is invalid.[4]

For every arm × case × repeat, retain the implementation commit, build hash, configuration, input/fault manifest, CPU and simulator mode, ROI markers where relevant, stdout/stderr, trace, decision/order record, state/checkpoint digest, disposition, prior-valid-state evidence for negative cases, exit status, SHA-256 inventory, and an immutable status of `accepted`, `rejected as designed`, `failed`, `timed out`, or `invalid/inconclusive`.[4]

## 8. Supplementary-evidence index

If—and only if—the live form permits a repository or supplementary-material link, point reviewers to the following order:

| Priority | Evidence document | Purpose |
|---:|---|---|
| 1 | `docs/submission/chiplet-summit-2027-owner-review-package.md` | This human-review packet. |
| 2 | `docs/validation/cherry-cross-domain-mechanism-proof-20260823.md` | Completed mechanism proof versus future comparative-value boundary. |
| 3 | `docs/validation/cherry-kvm-full-matrix-evidence-20260822.md` | KVM-to-Timing full-system SimCXL behavioral evidence. |
| 4 | `docs/validation/cherry-controlled-gem5-matrix-evidence-20260822.md` | Separate controlled TimingSimpleCPU model evidence. |
| 5 | `docs/validation/cherry-execution-mode-reconciliation-20260823.md` | Execution-domain separation. |
| 6 | `docs/validation/cherry-measurement-claim-matrix-20260823.md` | Claim controls. |
| 7 | `docs/validation/cherry-scl-lod-derived-timing-differences-20260823.md` | Reference-model timing means and derivation boundary. |
| 8 | `docs/validation/ssdd-comparative-value-validation-plan-20260823.md` | Planned, not executed, fair comparative campaign. |
| 9 | `docs/validation/ssdd-comparative-local-policy-matrix-evidence-20260823.md` | Completed bounded local result; explicitly no value winner. |

Do not provide credentials, private data, unpublished infrastructure details, generated guest disks, or unrequested raw artifacts.

## 9. Live-form completion gate

The official 2027 Call page has not yet supplied the fields that determine the final paste-and-submit configuration. The following items must be copied from the live form, not inferred from prior years: deadline, abstract and title limits, category list, supplementary-material rule, copyright/privacy consent, presenter requirements, and speaker-slide format.[7]

| Step | Owner action | Package action |
|---:|---|---|
| 1 | Open the official 2027 call/form. | Capture visible fields, category list, limits, deadline, consent, and any upload rule. |
| 2 | Confirm presenter details and biography. | Select A, B, or C using the live character counter. |
| 3 | Confirm the selected category. | Recheck every sentence against the measurement ledger in Section 6. |
| 4 | Decide whether supplementary material is allowed. | Add only the permitted evidence link(s) from Section 8. |
| 5 | Read consent and final preview. | Submit only after explicit owner confirmation. |

No AI author, presenter, affiliation, or contributor attribution is included in this package.

## References

[1] [Cross-domain SSDD mechanism proof](../validation/cherry-cross-domain-mechanism-proof-20260823.md)  
[2] [Controlled gem5 matrix evidence](../validation/cherry-controlled-gem5-matrix-evidence-20260822.md)  
[3] [KVM full SimCXL matrix evidence](../validation/cherry-kvm-full-matrix-evidence-20260822.md)  
[4] [SSDD comparative-value validation plan](../validation/ssdd-comparative-value-validation-plan-20260823.md)  
[5] [Cherry measurement claim matrix](../validation/cherry-measurement-claim-matrix-20260823.md)  
[6] [Chiplet Summit 2027 abstract variants](chiplet-summit-2027-abstract-variants.md)  
[7] [Chiplet Summit 2027 requirements status](chiplet-summit-2027-requirements-status.md)
[8] [Local comparative policy-matrix evidence](../validation/ssdd-comparative-local-policy-matrix-evidence-20260823.md)
[9] [Blinded diagnostic and policy review protocol](../validation/ssdd-comparative-human-review-protocol-20260823.md)
