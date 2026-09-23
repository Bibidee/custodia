import hashlib
import json

CONTRACT = "contracts/custodia.py"
DELIVERABLE = b"Custodia hardening fixture is complete."
EVIDENCE = b"Independent evidence confirms the Custodia hardening fixture is complete."


def digest(value):
    return "0x" + hashlib.sha256(value).hexdigest()


def deployed(direct_deploy, direct_vm):
    direct_vm.warp("2026-09-22T12:00:00Z")
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = None
    return contract


def create(contract, direct_vm, sponsor, consumer, escrow_id="H-001", window=3600):
    direct_vm.sender = sponsor
    direct_vm.value = 10**18
    contract.create_escrow(
        escrow_id, consumer, consumer,
        "https://deliverable.example/h.txt", digest(DELIVERABLE),
        "https://evidence.example/h.txt", digest(EVIDENCE),
        "Hardening fixture is complete.", window,
    )
    direct_vm.value = 0


def web_ok(direct_vm):
    direct_vm.mock_web("https://deliverable.example/h.txt", {"status": 200, "body": DELIVERABLE})
    direct_vm.mock_web("https://evidence.example/h.txt", {"status": 200, "body": EVIDENCE})


def llm_ok(direct_vm, result=None):
    direct_vm.mock_llm("Hardening fixture", json.dumps(result or {
        "deliverable_match": "yes", "evidence_support": "yes", "risk": "no",
        "confidence": 90, "rationale": "Exact verified fixture."
    }))


def test_structured_output_normalization_and_retry(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deployed(direct_deploy, direct_vm)
    create(contract, direct_vm, direct_alice, direct_bob)
    web_ok(direct_vm)
    direct_vm.mock_llm("Hardening fixture", "```json\n" + json.dumps({"result": {
        "deliverable_match": " YES ", "evidence_support": "YES", "risk": "NO",
        "confidence": "90", "rationale": "Exact verified fixture.", "provider_note": "ignored metadata"
    }}) + "\n```")
    direct_vm.sender = direct_alice
    contract.review("H-001")
    assert contract.get_escrow("H-001")["status"] == "approved"


def test_retryable_can_retry_and_stranger_cannot_refund_early(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deployed(direct_deploy, direct_vm)
    create(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web("https://deliverable.example/h.txt", {"status": 503, "body": b""})
    direct_vm.mock_web("https://evidence.example/h.txt", {"status": 200, "body": EVIDENCE})
    direct_vm.sender = direct_alice
    contract.review("H-001")
    assert contract.get_escrow("H-001")["status"] == "retryable"
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert():
        contract.settle("H-001")
    direct_vm.clear_mocks()
    web_ok(direct_vm)
    llm_ok(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("H-001")
    assert contract.get_escrow("H-001")["status"] == "approved"


def test_unauthorized_review_and_invalid_creation_inputs(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deployed(direct_deploy, direct_vm)
    create(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert():
        contract.review("H-001")
    direct_vm.sender = direct_alice
    direct_vm.value = 1
    with direct_vm.expect_revert():
        contract.create_escrow("H-002", direct_bob, direct_bob, "http://bad.example/x", digest(DELIVERABLE), "https://evidence.example/h.txt", digest(EVIDENCE), "brief", 3600)
    with direct_vm.expect_revert():
        contract.create_escrow("H-003", direct_bob, direct_bob, "https://deliverable.example/h.txt", "0x1234", "https://evidence.example/h.txt", digest(EVIDENCE), "brief", 3600)
    direct_vm.value = 0


def test_expire_pending_and_approved_recovery(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deployed(direct_deploy, direct_vm)
    import importlib
    contract_gl = importlib.import_module(contract.__class__.__module__).gl
    create(contract, direct_vm, direct_alice, direct_bob, "H-002", 3600)
    direct_vm.warp("2027-01-01T00:00:01Z")
    contract_gl.message_raw["datetime"] = "2027-01-01T00:00:01Z"
    direct_vm.sender = direct_alice
    contract.expire("H-002")
    assert contract.get_escrow("H-002")["status"] == "settled"
    direct_vm.warp("2026-09-22T12:00:00Z")
    contract_gl.message_raw["datetime"] = "2026-09-22T12:00:00Z"
    create(contract, direct_vm, direct_alice, direct_bob, "H-003", 3600)
    web_ok(direct_vm)
    llm_ok(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("H-003")
    direct_vm.warp("2027-01-01T00:00:01Z")
    contract_gl.message_raw["datetime"] = "2027-01-01T00:00:01Z"
    contract.expire("H-003")
    assert contract.get_escrow("H-003")["status"] == "settled"


def test_validator_disagreement_is_not_approval(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deployed(direct_deploy, direct_vm)
    create(contract, direct_vm, direct_alice, direct_bob, "H-004")
    web_ok(direct_vm)
    llm_ok(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("H-004")
    assert direct_vm.run_validator(leader_result={"kind": "analysis", "result": {
        "deliverable_match": "no", "evidence_support": "no", "risk": "yes",
        "confidence": 90, "rationale": "Different blocking reason."
    }}) is False

    direct_vm.clear_mocks()
    web_ok(direct_vm)
    llm_ok(direct_vm, {"deliverable_match": "no", "evidence_support": "yes", "risk": "no", "confidence": 90, "rationale": "Unsupported match."})
    create(contract, direct_vm, direct_alice, direct_bob, "H-005")
    direct_vm.sender = direct_alice
    contract.review("H-005")
    assert direct_vm.run_validator(leader_result={"kind": "analysis", "result": {
        "deliverable_match": "no", "evidence_support": "no", "risk": "yes",
        "confidence": 90, "rationale": "Another safe blocking reason."
    }}) is True
