import hashlib
import json

CONTRACT = "contracts/custodia.py"
DELIVERABLE = b"Custodia milestone M-001 deliverable is complete."
EVIDENCE = b"Independent evidence confirms milestone M-001 deliverable is complete."


def digest(value):
    return "0x" + hashlib.sha256(value).hexdigest()


def deploy(direct_deploy, direct_vm):
    direct_vm.warp("2026-09-22T12:00:00Z")
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = None
    return contract


def setup(contract, direct_vm, direct_alice, direct_bob, value=10**18):
    direct_vm.sender = direct_alice
    direct_vm.value = value
    contract.create_escrow(
        "M-001", direct_bob, direct_bob,
        "https://deliverable.example/m001.txt", digest(DELIVERABLE),
        "https://evidence.example/m001.txt", digest(EVIDENCE),
        "Milestone M-001 is complete.", 21600,
    )
    direct_vm.value = 0


def configure(direct_vm, result=None):
    direct_vm.mock_web("https://deliverable.example/m001.txt", {"status": 200, "body": DELIVERABLE})
    direct_vm.mock_web("https://evidence.example/m001.txt", {"status": 200, "body": EVIDENCE})
    direct_vm.mock_llm("Milestone M-001", json.dumps(result or {
        "deliverable_match": "yes", "evidence_support": "yes", "risk": "no",
        "confidence": 90, "rationale": "The verified evidence supports the exact deliverable."
    }))


def test_create_read_and_approve(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_deploy, direct_vm)
    setup(contract, direct_vm, direct_alice, direct_bob)
    assert contract.get_escrow("M-001")["status"] == "pending"
    configure(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("M-001")
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert():
        contract.settle("M-001")
    assert contract.get_escrow("M-001")["status"] == "approved"


def test_consumer_only_settlement_and_replay_rejection(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_deploy, direct_vm)
    setup(contract, direct_vm, direct_alice, direct_bob)
    configure(direct_vm, {"deliverable_match": "no", "evidence_support": "no", "risk": "yes", "confidence": 90, "rationale": "The evidence does not support the exact deliverable."})
    direct_vm.sender = direct_alice
    contract.review("M-001")
    direct_vm.sender = direct_alice
    contract.settle("M-001")
    assert contract.get_escrow("M-001")["status"] == "settled"
    with direct_vm.expect_revert():
        contract.settle("M-001")


def test_artifact_failure_is_retryable_and_never_approves(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    setup(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web("https://deliverable.example/m001.txt", {"status": 503, "body": b""})
    direct_vm.mock_web("https://evidence.example/m001.txt", {"status": 200, "body": EVIDENCE})
    direct_vm.sender = direct_alice
    contract.review("M-001")
    assert contract.get_escrow("M-001")["status"] == "retryable"


def test_pending_cancel_refunds_and_approved_cancel_reverts(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    setup(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.cancel("M-001")
    assert contract.get_escrow("M-001")["status"] == "cancelled"
    with direct_vm.expect_revert():
        contract.cancel("M-001")
