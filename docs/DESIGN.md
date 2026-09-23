# Custodia design

Custodia combines deterministic escrow accounting with GenLayer semantic
consensus. The sponsor provides a beneficiary, designated consumer, exact
deliverable URL/hash, exact evidence URL/hash, and a bounded review window.

Validators independently fetch both artifacts and review only the verified
content. The approval tuple requires `deliverable_match=yes`,
`evidence_support=yes`, `risk=no`, and confidence at least 75. Rationale is
explanatory and never authorizes payment. Validator disagreement, malformed
model output, unavailable sources, or hash mismatch cannot approve.

All payout paths zero the deposited ledger and persist state before calling the
single GEN transfer helper. Approval pays the beneficiary after the review
window; blocked or retryable outcomes refund the sponsor; cancellation refunds
only a still-pending escrow. A zero ledger prevents replayed settlement.

Custodia does not prove real-world identity, guarantee source availability, or
replace downstream authorization. Integrators must inspect the canonical state
and treat only `consumed` as a completed payout.
