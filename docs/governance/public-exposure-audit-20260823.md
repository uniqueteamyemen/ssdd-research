# Public Repository Exposure Audit — 23 August 2026

**Status:** Completed visibility safeguard.
**Scope:** GitHub repositories owned by `uniqueteamyemen` that were public at the start of this audit.

## Decision

The public repositories below contained research implementation, product implementation, operational evidence, product design, or domain-specific system material whose public availability was not required for the independent blinded review. Each was changed to **private**.

| Repository | Public material observed during audit | Visibility decision |
|---|---|---|
| `ssdd-research` | SSDD reference implementation, detailed evidence corpus, simulator/reproduction material, comparative policy code, and submission materials. | **Private** |
| `paylock-core` | PayLock core implementation, enforcement/audit material, Docker/CI paths, integration evidence, and product runtime artifacts. | **Private** |
| `yaqeen-platform` | Product/platform source, production-design and release material, and PayLock/Yaqeen integration paths. | **Private** |
| `Yemen-Drug` | Domain-specific application source and intelligence/matching-engine design material. | **Private** |
| `HC-CXL-Sovereign` | Protocol/evidence-pack material for a CXL/memory-pool systems direction. | **Private** |

The audit did not identify a tracked private-key, cloud-key, common webhook-secret, or `.env` filename pattern in the checked heads. That is not a substitute for secret rotation or a historical Git/third-party-cache review.

## Sole retained public repository

| Repository | Purpose | Deliberate contents | Deliberate exclusions |
|---|---|---|---|
| `ssdd-blinded-review` | Let qualified independent reviewers complete a bounded public A/B/C decision-record review without contacting the owner. | Eighteen blinded JSON packets, checksum inventory, review instructions, response template, narrow copyright/review-use notice, and copy-ready outreach text. | SSDD source, PayLock/Yaqeen source, raw Cherry evidence, gem5/SimCXL source/configuration, production details, credentials, customer data, and the unblinding key. |

The public review repository is available at <https://github.com/uniqueteamyemen/ssdd-blinded-review>. Its public response workflow is intentionally limited to the stated review task. It does not disclose the A/B/C mapping and does not make a hardware, performance, or product claim.

## Residual risk and operating rule

Making a repository private stops normal future public access, but it cannot retract any clone, fork, screenshot, cache, archive, or copy created while a repository was public. The correct ongoing rule is therefore:

> Keep implementation, raw evidence, commercial product material, configuration, and future research private by default. Publish only an intentionally curated minimal artifact when a specific public purpose requires it.

Before any future public release, review the exact file tree, confirm that a license/notice matches the intended grant, scan for secrets and operational details, and ensure a separate public repository contains only material necessary for that release.
