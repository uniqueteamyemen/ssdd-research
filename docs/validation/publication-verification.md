# SSDD Public Publication Verification

**Checked:** 17 August 2026
**Public repository:** <https://github.com/uniqueteamyemen/ssdd-research>
**Active reproducible baseline tag:** [`prehardware-baseline-v0.1.1`](https://github.com/uniqueteamyemen/ssdd-research/tree/prehardware-baseline-v0.1.1)

## Verification record

The public repository page was checked without repository-management access. It displayed the repository as public and exposed the `docs`, `evidence`, `reference`, `scripts`, and `simulation/gem5` trees. The rendered README linked to the baseline record, the post-baseline reference record, and the retained gem5 rerun directory.

| Check | Method | Outcome |
|---|---|---|
| Public availability | Direct anonymous repository page request | Repository visible as public. |
| Baseline provenance | Remote branch and annotated-tag resolution | `main` contains the publication correction; `prehardware-baseline-v0.1.1` is the active reproducible baseline. |
| Documentation paths | [`scripts/verify_doc_links.py`](../../scripts/verify_doc_links.py) | All relative Markdown targets resolve in the repository. |
| Public artifact paths | Repository-wide scan of public Markdown documentation | No host-workspace or external gem5-checkout paths remain in the published validation records. |
| Artifact integrity | SHA-256 verification inside each evidence directory | Retained gem5 rerun and post-baseline reference-extension files match their inventories. |

This verification confirms public accessibility and repository-internal traceability only. It does not alter the stated model boundaries or convert simulation and reference-model evidence into hardware, network, security, or production claims.
