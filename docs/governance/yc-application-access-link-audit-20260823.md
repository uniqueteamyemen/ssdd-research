# YC Application Access-Link Audit — 23 August 2026

**Status:** Observation only. No application, demo, repository, or account field was edited.

## Observed submitted access fields

| Application field | Submitted value | Observation |
|---|---|---|
| Company URL | `https://github.com/uniqueteamyemen` | This is the owner account page, not a dedicated PayLock repository. After the repository privacy safeguard, its only public repository is the minimal SSDD blinded-review packet. |
| Product/demo link | `https://yaqeen-platform-production.up.railway.app/demo.html` | An unauthenticated HTTP check returned `404` on 23 August 2026. |

## Interpretation

The currently submitted YC application cannot provide direct public access to PayLock source because `paylock-core` and `yaqeen-platform` are private by design. This protects the proprietary product but makes the company URL and demo-link presentation a separate product/application decision.

No conclusion is drawn about the state of the deployed application beyond the observed `404` response for the submitted path. No YC update, submission, edit, or external communication was made.
