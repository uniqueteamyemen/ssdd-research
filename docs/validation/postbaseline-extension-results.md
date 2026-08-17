# SSDD Post-Baseline Reference Extensions — Research Record

**Status:** completed supplementary reference-model record.  
**Relation to baseline:** executed after the immutable annotated tag [`prehardware-baseline-v0.1.0`](prehardware-baseline-release.md). It does not modify or broaden the claims of that baseline.  
**Interpretation:** each result below concerns the named single-process reference harness, its deterministic seed, and its retained output. It is not evidence of a distributed runtime, a Rust runtime, network behavior, hardware arithmetic, CXL behavior, security resilience, or production readiness.

## Purpose and retained record

These supplementary checks address three useful but bounded questions: whether random arrival order can affect an entire reference hash chain; whether a preserved reference checkpoint reproduces its subsequent suffix after a modelled no-commit/deferred condition; and whether the retained Q32.32 arithmetic agrees with an independently written integer oracle across a deterministic vector set. The execution manifest, individual JSON records, retained audit trail, run log, and SHA-256 inventory are stored under [`evidence/prehardware/postbaseline-extensions-v0.1.0/`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/).

| Extension | Method | Result | Retained artifact |
|---|---|---|---|
| Full-chain arrival-order stress | 256 independently seeded arrival permutations; 100 epochs per permutation | All 256 chains matched the same final hash `34b7958a64082c326ba3a7cab44468ae9564c7ec2072f88533e10426e23f65c2`. | [`ordering-chain-stress.json`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/ordering-chain-stress.json) |
| Four-key collision guard | Vary each ordering-key component separately; submit an exact key duplicate with a different payload | The distinct components sorted canonically; the exact duplicate was rejected. | [`ordering-chain-stress.json`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/ordering-chain-stress.json) |
| Modelled no-commit checkpoint resumption | Four named reference fault categories; compare a re-run from the retained prefix through epoch 19 | Each case retained the epoch-11 checkpoint hash and reproduced the following reference suffix. | [`fault-recovery.json`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/fault-recovery.json) |
| Q32.32 differential arithmetic | 10,000 deterministic signed 64-bit input pairs, seed `0x5A5D432` | Saturated addition and multiplication matched the independent Python integer oracle for every vector. | [`q32-differential.json`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/q32-differential.json) |

## Interpretation boundary

The ordering record exercises the reference sorting and ledger functions within one process; it does not introduce concurrent nodes, packets in transit, or a network scheduler. The checkpoint record represents the documented no-commit/deferred recovery rule by re-running from the same valid reference prefix. It is not an injected process, storage, or network failure and must not be described as such. The arithmetic oracle is independent Python integer code, not the unavailable external Q32.32 core and not a hardware arithmetic test.

> The justified statement is limited to deterministic behavior of the retained reference code under these seeds and inputs. The next evidence class for a distributed claim remains a separately defined multi-process network matrix; it is not included here.

## Reproduction

Run the extended reference path from the repository root. The runner writes fresh files below `.local-results/`, leaving the committed audit record untouched.

```bash
SSDD_RESULTS_DIR="$PWD/.local-results/postbaseline-extensions-v0.1.0" \
  ./scripts/run_prehardware_extended.sh
```

The SHA-256 inventory in [`SHA256SUMS`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/SHA256SUMS) binds the retained files in this record. A rerun must be recorded as a new evidence directory if its source, compiler, environment, input, or result changes.
