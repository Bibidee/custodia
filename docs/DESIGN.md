# Custodia design

Custodia combines deterministic escrow accounting with GenLayer semantic
consensus. The sponsor provides a beneficiary, designated consumer, exact
deliverable URL/hash, exact evidence URL/hash, and a bounded review window.

Validators independently fetch both artifacts and review only the verified
content. Persistent fields are copied into an in-memory review snapshot before
nondeterministic execution. The approval tuple requires
`deliverable_match=yes`, `evidence_support=yes`, `risk=no`, and confidence at
least 75. Rationale is explanatory and never authorizes payment. Validator
disagreement, malformed model output, unavailable sources, or hash mismatch
cannot approve.

Reviews are limited to three attempts. A retryable review can be retried by
the sponsor or consumer before the review deadline. After the deadline,
expiry recovery refunds the sponsor. Approved releases require the designated
consumer after the review window; an additional recovery deadline prevents
consumer abandonment from locking funds forever. All payout paths zero the
deposited ledger before calling the single GEN transfer helper. A zero ledger
prevents replayed settlement.

Custodia does not prove real-world identity, guarantee source availability,
prove DNS/redirect safety, or replace downstream authorization. It currently
does not emit lifecycle events; integrators should poll canonical state and
treat only `consumed` as a completed beneficiary payout.
