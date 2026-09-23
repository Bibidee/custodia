from pathlib import Path
import ast
import hashlib
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
contracts = list((root / "contracts").glob("*.py"))
if len(contracts) != 1:
    raise SystemExit(f"expected exactly one deployable source, found {len(contracts)}")
source = contracts[0]
ast.parse(source.read_text(encoding="utf-8"))
subprocess.run([sys.executable, "-m", "pytest", "tests", "-q"], cwd=root, check=True)
lint = shutil.which("genvm-lint") or shutil.which("genvm-lint.exe")
if not lint:
    sibling = Path(sys.executable).with_name("genvm-lint.exe" if sys.platform == "win32" else "genvm-lint")
    lint = str(sibling) if sibling.exists() else None
if not lint:
    raise SystemExit("genvm-lint is required for preflight")
subprocess.run([lint, "check", str(source), "--json"], cwd=root, check=True)
(root / "artifacts").mkdir(exist_ok=True)
subprocess.run([lint, "schema", str(source), "--output", "artifacts/custodia.abi.json"], cwd=root, check=True)
print("contract_sha256=" + hashlib.sha256(source.read_bytes()).hexdigest())
print("preflight passed")
