# Derived Timing Differences — SCL-01 and LOD-01

**Status:** Derived from retained source JSON, not a new experiment.  
**Source artifact:** `evidence/native-reference/cherry-scale-load1-20260822/inner/scaling-load.json`  
**Source domain:** `native_reference_wallclock`  
**Source limitation:** The JSON itself states that values are reference-model measurements, not NIC bandwidth, distributed convergence, or hardware timing.

## What this derivation measures

The retained JSON provides **mean internal timing components per point**: `T_agg`, `T_fuse`, `T_ssc`, and `T_total`. The differences below are endpoint differences calculated directly from those stored means. They are valid descriptions of the declared native-reference model run.

They are not device latency, CXL latency, fabric latency, service latency, KVM full-system timing, or a baseline-versus-SSDD improvement claim.

## SCL-01 — 8 to 128 logical nodes

| Stored mean component | 8 nodes (µs) | 128 nodes (µs) | Difference (µs) | Change |
|---|---:|---:|---:|---:|
| `T_agg` | 2.205 | 29.550 | +27.345 | +1240.136% |
| `T_fuse` | 0.805 | 0.739 | -0.066 | -8.199% |
| `T_ssc` | 9.143 | 147.336 | +138.193 | +1511.462% |
| `T_total` | 12.152 | 177.625 | +165.473 | +1361.694% |

The stored reference event-rate field moves from 793,259.67 to 872,231.98 events/s (+9.955%). Packets per epoch and modeled bytes per epoch increase by the model-defined 16× factor, from 32 to 512 packets and from 896 to 14,336 bytes respectively. Every stored point reports `epoch_success_rate = 1.0`.

## LOD-01 — 1,000 to 100,000 input events/s-equivalent

| Stored mean component | 1,000 target (µs) | 100,000 target (µs) | Difference (µs) | Change |
|---|---:|---:|---:|---:|
| `T_agg` | 0.160 | 5.921 | +5.761 | +3600.625% |
| `T_fuse` | 0.593 | 0.559 | -0.034 | -5.734% |
| `T_ssc` | 0.520 | 26.605 | +26.085 | +5016.346% |
| `T_total` | 1.274 | 33.085 | +31.811 | +2496.939% |

The stored observed reference-rate field moves from 296,198.00 to 900,909.50 events/s (+204.158%). Packets per epoch and modeled bytes per epoch increase by the model-defined 100× factor, from 1 to 100 packets and from 28 to 2,800 bytes respectively. Every stored point reports `epoch_success_rate = 1.0`.

## Jitter and percentile status

| Requested metric | Available from retained SCL-01 / LOD-01 artifact? | Reason |
|---|---|---|
| Mean internal component timing | Yes | `timing_mean_us` is retained at each declared point. |
| Endpoint timing differences | Yes | Calculated directly from retained means; reproducible by the included derivation script. |
| Per-epoch jitter, standard deviation, p95, p99, or histogram | No | The bundle contains per-point means only. It does not retain individual epoch timing samples or a timing distribution. |
| Device/CXL/NIC latency or throughput | No | The source domain is explicitly `native_reference_wallclock` with modelled counters. |

## Submission-safe wording

> In a retained native-reference scale/load exercise, the model’s stored mean `T_total` increased from 12.152 µs at 8 logical nodes to 177.625 µs at 128 logical nodes, and from 1.274 µs at the 1,000 events/s-equivalent input target to 33.085 µs at 100,000. These are reference-model internal timing means and not physical or full-system latency measurements. The retained bundle has no per-epoch timing distribution, so it does not support jitter or percentile claims.

## Reproduction

Run:

```bash
node tools/derive-scl-lod-timing-deltas.mjs \
  evidence/native-reference/cherry-scale-load1-20260822/inner/scaling-load.json
```

The resulting JSON is retained at [`cherry-scl-lod-timing-deltas-20260823.json`](cherry-scl-lod-timing-deltas-20260823.json).

## Related evidence

- [`cherry-scale-load-native-reference-evidence-20260822.md`](cherry-scale-load-native-reference-evidence-20260822.md)
- [`cherry-nine-test-campaign-evidence-index-20260822.md`](cherry-nine-test-campaign-evidence-index-20260822.md)
- [`cherry-measurement-claim-matrix-20260823.md`](cherry-measurement-claim-matrix-20260823.md)
