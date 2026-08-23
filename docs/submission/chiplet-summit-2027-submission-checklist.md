# Chiplet Summit 2027 — Submission Package Checklist

**Status:** Preparation checklist. The official 2027 form is not yet populated with requirements as of 23 August 2026.

## Content package

| File or field | Current state | Required action before submission |
|---|---|---|
| Presentation title | Drafted | Confirm title against the final 2027 category. |
| Abstract | Drafted | Paste only after checking the 2027 character limit and required fields. |
| Claim-boundary statement | Ready | Keep with the abstract, slides, and speaker notes. |
| Technical evidence index | Ready | Link to the fixed evidence documents and commits. |
| SCL-01 / LOD-01 timing-difference note | Ready | Describe only as native-reference mean internal timings. |
| KVM-to-Timing SimCXL matrix note | Ready | Describe only as full-system behavioral simulation. |
| Speaker biography | Not yet supplied | Obtain owner-approved biography. |
| Affiliation and contact details | Not yet supplied | Obtain owner-approved final spelling and contact details. |
| Copyright/privacy consent | Pending official 2027 form | Review and approve only when the official form appears. |
| Slides | Not started | Use the 2027 speaker template when supplied; do not rely on the 2026 template as a final format. |

## Technical support inventory

| Item | Repository record |
|---|---|
| Nine-ID evidence index | `docs/validation/cherry-nine-test-campaign-evidence-index-20260822.md` |
| KVM-to-Timing full-system behavioral matrix | `docs/validation/cherry-kvm-full-matrix-evidence-20260822.md` |
| CPU/KVM/CXL-mode reconciliation | `docs/validation/cherry-execution-mode-reconciliation-20260823.md` |
| Claim controls | `docs/validation/cherry-measurement-claim-matrix-20260823.md` |
| Derived SCL-01 / LOD-01 mean timing differences | `docs/validation/cherry-scl-lod-derived-timing-differences-20260823.md` |
| Reproducible derivation tool | `tools/derive-scl-lod-timing-deltas.mjs` |

## Final pre-submit checks

Before a human submits the form, confirm all of the following:

1. The 2027 form’s category, character limit, deadlines, author/presenter fields, and consent text have been copied from the official live form.
2. Every performance sentence uses the bounded wording in the claim matrix.
3. Every figure labels reference-model timing, SimCXL simulation, or full-system behavioral evidence accurately.
4. The named human presenter and affiliation are correct and owner-approved.
5. No document includes an AI tool as author, presenter, affiliation, or research contributor.
6. No submission is sent without explicit owner confirmation.
