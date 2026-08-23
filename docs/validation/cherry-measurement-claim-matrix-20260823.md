# SSDD Cherry Measurement Claim Matrix

**Use:** Submission-writing control sheet.  
**Evidence state:** Cherry artifacts reconciled at repository commit `f8134db080489876af68bfa7eae94c10475d70aa`.

| Proposed submission statement | Permitted now? | Required qualifier / evidence basis |
|---|---|---|
| “The work includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix.” | Yes | State that it is simulation, not physical CXL or hardware qualification. |
| “The matrix booted under KVM and switched to a Timing CPU before a guest-delimited ROI.” | Yes | Cite the retained KVM-to-Timing record and call it an execution-path fact, not a performance result. |
| “Three independently retained ROI-closed executions reproduced the declared five-cell semantic matrix.” | Yes | State that the result is acceptance/rejection behavioral reproducibility. |
| “A separate controlled gem5 matrix retained TimingSimpleCPU configurations.” | Yes | Identify it as syscall-emulation, model-specific timing-sensitivity and fault evidence. |
| “SSDD reduces latency, jitter, or p99.” | No | No preregistered baseline/control comparison, repetitions, statistical summary, or normalized metric result is retained. |
| “SSDD improves throughput or lowers overhead.” | No | Native-reference input targets and modeled counters are not measured fabric/network throughput or baseline-versus-SSDD overhead. |
| “The experiment used physical CXL Type-3 or FPGA hardware.” | No | `cxl-asic` and `cxl-fpga` identify simulator modes only. |
| “The `numCycles` values quantify a speed comparison.” | No | They are retained only to establish that the Timing CPU executed after the switch. |
| “The nine Cherry IDs are KVM performance benchmarks.” | No | The nine-ID index is reference-model evidence and explicitly separates the KVM full-system matrix. |

## Minimal safe method paragraph

> We evaluated SSDD in bounded pre-silicon execution domains. The retained corpus includes a Cherry-hosted full-system SimCXL/gem5 behavioral matrix that booted under KVM and switched to a Timing CPU before a guest-delimited region of interest, together with a separate syscall-emulation TimingSimpleCPU controlled matrix and nine reference-model records. We report semantic acceptance/rejection and reproducibility at the stated simulation scope; we do not report physical-CXL, FPGA, latency, jitter, throughput, or overhead claims.

## Before any quantitative extension

A later quantitative section must predeclare the baseline and SSDD configurations, measurement region, unit and clock basis, warm-up policy, repetitions, outlier policy, statistical summaries, and artifact inventory. The current corpus cannot be retroactively promoted into that campaign.

## Related records

- [`cherry-execution-mode-reconciliation-20260823.md`](cherry-execution-mode-reconciliation-20260823.md)
- [`cherry-kvm-full-matrix-evidence-20260822.md`](cherry-kvm-full-matrix-evidence-20260822.md)
- [`cherry-nine-test-campaign-evidence-index-20260822.md`](cherry-nine-test-campaign-evidence-index-20260822.md)
