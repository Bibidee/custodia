# Custodia

Custodia is a standalone GenLayer Intelligent Contract primitive for
hash-bound milestone escrow. A sponsor locks GEN against an exact deliverable
and evidence bundle. Validators independently fetch the committed raw bytes,
verify SHA-256 digests, and semantically decide whether the evidence supports
release.

The deterministic contract derives `approved`, `blocked`, or `retryable` from
the agreed bounded result. Approval is never based on a summary alone. Payout
logic follows the safe escrow order: read the deposited ledger, zero and save
it, then emit GEN. This makes duplicate settlement structurally impossible.

Terminal paths are deliberately small:

`pending -> approved -> consumed` (beneficiary payout after the review window)

`pending -> blocked|retryable -> settled` (sponsor refund)

`pending -> cancelled` (sponsor refund before review)

Every artifact is HTTPS, size bounded, UTF-8, and SHA-256 verified. External
availability and semantic uncertainty fail closed. This repository is an
early implementation pass; tests, preflight, lint, schema generation, and a
source-matched Studionet deployment are required before release.
