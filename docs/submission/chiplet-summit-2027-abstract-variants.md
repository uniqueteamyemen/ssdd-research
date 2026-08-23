# Chiplet Summit 2027 — Modular Abstract Variants

**Use:** Select the longest variant that fits the official 2027 form after its live character limit is visible.  
**Title:** **SSDD: Pre-Silicon Quantitative Behavioral Characterization of Distributed Memory-System Execution**

The variants below use the same claim boundary. They describe pre-silicon reference-model and SimCXL/gem5 behavioral evidence; they do not claim physical CXL, FPGA behavior, latency, jitter, percentile, throughput, baseline-versus-SSDD, or production results.

## Variant A — concise

SSDD is a pre-silicon study of shared containment and reference treatment for distributed memory-system execution. Its retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix that booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Three independently retained ROI-closed executions reproduced expected acceptance or rejection semantics across five declared memory/fault cells. Separate TimingSimpleCPU and native-reference exercises retain model-specific timing means and integrity evidence. The work reports bounded simulation behavior, not physical-CXL, FPGA, latency, jitter, throughput, or production claims.

## Variant B — standard

Distributed memory-system execution can fail at the boundary between local handling and the shared meaning of an event. SSDD is a pre-silicon systems-design study of shared containment and reference treatment for that boundary. The retained corpus separates its execution domains. A Cherry-hosted full-system SimCXL/gem5 matrix booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, five declared memory/fault cells reproduced their intended acceptance or rejection semantics: DRAM control, two accepted CXL simulator modes, an accepted interleave mode, and a proof-corruption rejection. A separate syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments. Native-reference scale/load records retain mean internal timing components across 8–128 logical nodes and 1,000–100,000 input events/s-equivalent. The contribution is an evidence-bounded characterization method that preserves configuration, simulation mode, ROI markers, semantic outcomes, and integrity records while keeping model timing separate from hardware or fabric performance. The work makes no physical-CXL, FPGA, latency, jitter, percentile, throughput, baseline-comparison, or production claim.

## Variant C — extended

Distributed memory-system execution must preserve a shared interpretation of an event even when local processing paths and memory placements differ. SSDD is a pre-silicon systems-design study of shared containment and reference treatment for this problem. Its evaluation is organized as bounded evidence domains rather than one undifferentiated performance claim.

The retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix. The guest booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, the five declared memory/fault cells reproduced their expected semantic outcomes: DRAM control, accepted CXL-ASIC simulator mode, proof-corruption rejection, accepted CXL-FPGA simulator mode, and accepted interleave mode. The CXL labels denote simulator modes, not physical devices. A separate syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments.

The retained native-reference scale/load exercise records mean internal timing components over 8–128 logical nodes and 1,000–100,000 input events/s-equivalent. Its stored mean `T_total` changes from 12.152 µs to 177.625 µs across the node endpoints and from 1.274 µs to 33.085 µs across the input endpoints. These are reference-model means, not device or fabric latency measurements. The retained bundle contains no per-epoch timing distribution and therefore supports neither jitter nor percentile claims.

The contribution is a reproducible, evidence-bounded characterization method: preserve the execution path, configuration, guest ROI markers, semantic acceptance/rejection, source hashes, manifests, and integrity checks; then keep reference-model timing distinct from hardware performance. The result is a pre-silicon basis for later controlled quantitative comparisons, not a replacement for them.

## Final-form selection rule

When the 2027 form becomes visible, count the selected variant exactly as the form does, including any title or field-specific accounting required by the form. Do not assume the historical 2026 3,768-character field is still the 2027 rule.

## Evidence anchors

- [`../validation/cherry-execution-mode-reconciliation-20260823.md`](../validation/cherry-execution-mode-reconciliation-20260823.md)
- [`../validation/cherry-measurement-claim-matrix-20260823.md`](../validation/cherry-measurement-claim-matrix-20260823.md)
- [`../validation/cherry-scl-lod-derived-timing-differences-20260823.md`](../validation/cherry-scl-lod-derived-timing-differences-20260823.md)
