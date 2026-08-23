# Private GitHub Repository Hardening Checklist

**Scope:** Private repositories holding SSDD, PayLock, Yaqeen, Yemen-Drug, and HC-CXL materials.
**Status:** Guidance only. No GitHub access, workflow, member, secret, or branch setting is changed by this document.

> Private visibility protects future normal public access. It does not protect a repository from an account takeover, an overprivileged collaborator, a leaked token, unsafe automation, or a copy made while the repository was public.

## Priority 0 — do these first

| Control | Exact action | Why it matters |
|---|---|---|
| Secure the owner account | Enable phishing-resistant two-factor authentication, preserve recovery codes offline, review active sessions/devices, and revoke any unrecognized OAuth app or personal-access token. Use a password manager and a unique password. | An owner takeover defeats every repository setting. |
| Reduce access | In each private repository, remove every collaborator who does not actively need access. Give `Read` only to viewers, `Write` only to active code contributors, and reserve `Admin` for the owner. Do not use a shared GitHub account. | Private collaborators can clone the full repository; `Admin` includes sensitive and destructive controls.[3] |
| Inventory and rotate secrets | Treat any credential ever committed, pasted into an Issue, Actions log, release, wiki, or public chat as potentially exposed. Revoke/rotate it at the provider first; only then consider history cleanup. | GitHub scans history and collaboration content for hard-coded secrets; rotation is the urgent remedy for an exposed credential.[1] |
| Stop committing runtime material | Ensure `.env`, private keys, connection strings, deployment exports, database dumps, payment/provider credentials, screenshots with personal data, and production logs are ignored and stored outside Git. | Private does not make sensitive runtime data appropriate for source control. |
| Remove tracked dependencies | Remove committed `node_modules/`, build output, downloaded evidence copies, and generated deployment artifacts where they are not essential provenance. Keep lockfiles, manifests, checksums, and source. | It shrinks the attack surface, unnecessary disclosure, and review burden. |

## Priority 1 — protect changes and automation

| Control | Recommended configuration | Operating rule |
|---|---|---|
| Default branch | Protect `main`: require pull requests, require at least one review when a second contributor exists, block force pushes, block branch deletion, require status checks where tests exist, and require a resolved conversation before merge. | Do not push directly to `main` for product, deployment, or security changes. |
| `CODEOWNERS` | Require owner review for `.github/workflows/**`, deployment files, infrastructure, package manifests/lockfiles, authentication, payment/provider adapters, and security configuration. | A workflow or deployment change is security-sensitive code. |
| GitHub Actions tokens | Set the repository default `GITHUB_TOKEN` permission to **read-only**. Grant write permissions only to the individual job that requires them. | GitHub recommends least privilege; anyone with write access can read repository secrets used by workflows.[2] |
| Third-party Actions | Allow only trusted actions and pin every external action to a full commit SHA, not just a mutable tag. | A full SHA is GitHub’s immutable reference recommendation for Actions.[2] |
| Dangerous triggers | Avoid `pull_request_target` and `workflow_run` unless necessary. Never check out or execute untrusted pull-request code in a privileged workflow. | These triggers can combine untrusted code with repository write permission or secrets.[2] |
| Self-hosted runners | Do not run untrusted or pull-request workloads on a runner that has production network access, credentials, SSH keys, or other private repositories. Prefer GitHub-hosted ephemeral runners. | A self-hosted runner can be persistently compromised by workflow code.[2] |
| Deployment environments | Put production deployment secrets in a protected environment; require a reviewer for production deployment and limit which branches can deploy. Prefer OIDC with short-lived cloud credentials rather than long-lived keys. | This separates a code merge from access to deployment secrets.[2] |

## Priority 2 — scan, monitor, and recover

| Control | Exact action | Cadence |
|---|---|---|
| Secret scanning / push protection | Enable where your GitHub plan supports it; add generic/custom patterns for DS&D-specific connection strings, provider webhooks, internal hostnames, and key formats. | Continuous; resolve every alert by revoking/rotating first.[1] |
| Dependabot and code scanning | Enable security updates/alerts for package manifests. Add CodeQL or an appropriate code scanner for active product repositories. | Continuous; review alerts weekly. |
| Actions review | Review workflow files, permitted Actions, workflow logs, and repository/organization secrets. Delete logs containing sensitive data after rotation. | Monthly and after every workflow change.[2] |
| Account and repository audit | Review collaborators, deploy keys, OAuth apps, personal-access tokens, SSH keys, branch-protection exceptions, webhooks, releases, Pages, package registries, and forks. | Monthly; immediately after any personnel or vendor change. |
| Backup and recovery | Keep encrypted offline or separate-account backups of source and essential evidence. Test restoring a private repository and do not depend on a single laptop or a single GitHub account. | Quarterly restore test. |

## Repository-specific operating policy

| Repository type | Keep private | May be public only in a curated separate repository |
|---|---|---|
| PayLock / Yaqeen | Source, provider adapters, test evidence containing operational details, payment/webhook material, deployment design, environment names, and live integration traces. | A high-level product page, non-operational architecture diagram, or approved demo with no credentials or internal route details. |
| SSDD / HC-CXL | Implementations, raw evidence, simulator configs, reproduction maps, Cherry provenance, comparison source, draft claims, and unfiled research. | A deliberately minimal review packet, approved abstract, or selected non-reproducible high-level evidence summary. |
| Yemen-Drug | Catalog data, matching rules, provider/partner material, operational workflows, user data, and backlog. | A carefully reviewed public information page with no catalog, user, or partner data. |

## Release gate — use before sharing anything

Before a link, ZIP, repository, release, issue attachment, or GitHub Page becomes public, answer all of these:

1. Is this the **minimum** material required for the stated public purpose?
2. Does it contain source, a reproducible algorithm, raw evidence, credentials, internal hostnames, customer/provider data, logs, screenshots, or a mapping key?
3. Is the license/notice intentional? If not, do not publish it.
4. Has an owner reviewed the exact file list, not only the README?
5. Can the public purpose be met by a new minimal repository instead of changing a product/research repository to public?

If any answer is uncertain, keep it private and create a curated review-only release instead.

## What privacy cannot undo

Changing a repository to private stops normal new public browsing and cloning. It cannot revoke copies, forks, clones, screenshots, archives, search indexes, credentials, or artifacts that were already exposed. For that reason, when a secret may have been exposed, **rotate it first**; do not rely on private visibility or history rewriting as the primary remediation.[1]

## Official references

[1] [GitHub Docs — Secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)
[2] [GitHub Docs — Secure use reference for GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use)
[3] [GitHub Docs — Repository roles for organizations](https://docs.github.com/organizations/managing-user-access-to-your-organizations-repositories/repository-roles-for-an-organization)
