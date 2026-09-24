import { createRequire } from "node:module";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { createHash } from "node:crypto";
import { setTimeout as delay } from "node:timers/promises";

const cliRoot = join(process.env.APPDATA, "npm", "node_modules", "genlayer");
const cliRequire = createRequire(join(cliRoot, "package.json"));
const [{ createClient }, { studionet }, { privateKeyToAccount }] = await Promise.all([
  import(pathToFileURL(cliRequire.resolve("genlayer-js"))),
  import(pathToFileURL(cliRequire.resolve("genlayer-js/chains"))),
  import(pathToFileURL(cliRequire.resolve("viem/accounts"))),
]);
const keytar = cliRequire("keytar");

const contractAddress = "0xbbE551d0197279E17dC0Ed82b876371856EF03cd";
const accountName = process.env.CUSTODIA_DIAG_ACCOUNT || "fresh-bob";
const key = await keytar.getPassword("genlayer-cli", `account:${accountName}`);
if (!key) throw new Error(`Unlocked CLI keychain entry unavailable for ${accountName}`);
const account = privateKeyToAccount(key);
const client = createClient({ chain: studionet, endpoint: "https://studio.genlayer.com/api", account });

const artifacts = [
  {
    url: "https://raw.githubusercontent.com/Bibidee/custodia/2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-deliverable.txt",
    expected: "0xb7071f431f30123d20f407f5819e7626792e9e6a8c26e3d7bb51f8cdc5ebeed8",
  },
  {
    url: "https://cdn.jsdelivr.net/gh/Bibidee/custodia@2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-evidence.txt",
    expected: "0x090299995751c5a4e8c06fa36259b1e9ded8a0f544cbf4bda2af1ae8d7e035cd",
  },
];

async function verifyArtifact(artifact) {
  const response = await fetch(artifact.url, { redirect: "follow" });
  if (!response.ok) throw new Error(`Artifact fetch failed with HTTP ${response.status}`);
  const bytes = Buffer.from(await response.arrayBuffer());
  const actual = `0x${createHash("sha256").update(bytes).digest("hex")}`;
  new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  if (actual !== artifact.expected) throw new Error(`Artifact hash mismatch for ${artifact.url}`);
  return { url: artifact.url, sha256: actual, bytes: bytes.length };
}

function status(tx) {
  return tx.statusName || tx.status_name;
}

function txSummary(tx) {
  return {
    hash: tx.hash,
    status: status(tx),
    consensus: tx.result_name || tx.resultName,
    execution: tx.consensus_data?.leader_receipt?.[0]?.execution_result,
  };
}

async function wait(hash) {
  for (let attempt = 0; attempt < 180; attempt += 1) {
    await delay(10_000);
    const tx = await client.getTransaction({ hash });
    if (["FINALIZED", "UNDETERMINED", "CANCELED"].includes(status(tx))) return tx;
  }
  throw new Error(`Timed out waiting for ${hash}`);
}

async function write(functionName, args, value = 0n) {
  const hash = await client.writeContract({
    address: contractAddress,
    functionName,
    args,
    value,
    consensusMaxRotations: 5,
  });
  return wait(hash);
}

async function read(id) {
  return client.readContract({
    address: contractAddress,
    functionName: "get_escrow",
    args: [id],
    transactionHashVariant: "latest-final",
  });
}

const info = await client.readContract({ address: contractAddress, functionName: "get_info" });
if (info.version !== "0.2.5") throw new Error(`Expected v0.2.5, received ${info.version}`);
const verified = await Promise.all(artifacts.map(verifyArtifact));
const id = `CUSTODIA-V25-PROMPT-${Date.now()}`;
const brief = "For this completed Custodia test milestone, determine whether the exact committed deliverable is supported by the independent evidence and ready for beneficiary release.";

console.log(JSON.stringify({ step: "setup", version: info.version, contract: contractAddress, proposer: account.address, escrowId: id, artifacts: verified }));

const proposal = await write("create_escrow", [
  id,
  account.address,
  account.address,
  artifacts[0].url,
  artifacts[0].expected,
  artifacts[1].url,
  artifacts[1].expected,
  brief,
  3600n,
], 1_000_000_000_000_000n);
if (status(proposal) !== "FINALIZED" || proposal.consensus_data?.leader_receipt?.[0]?.execution_result !== "SUCCESS") {
  throw new Error("v0.2.5 proposal did not finalize successfully");
}
const pending = await read(id);
if (pending.status !== "pending" || pending.deposited !== "1000000000000000") {
  throw new Error("v0.2.5 proposal state or deposit did not match");
}
console.log(JSON.stringify({ step: "proposal", ...txSummary(proposal), state: pending }));

const review = await write("review", [id]);
if (!["FINALIZED", "UNDETERMINED"].includes(status(review))) {
  throw new Error("v0.2.5 review ended in an unexpected transaction status");
}
const reviewed = await read(id);
console.log(JSON.stringify({ step: "review", ...txSummary(review), state: reviewed }));

if (reviewed.status === "pending") {
  const refund = await write("cancel", [id]);
  console.log(JSON.stringify({ step: "cancel_after_unresolved_review", ...txSummary(refund), state: await read(id) }));
} else if (reviewed.status === "blocked" || reviewed.status === "retryable") {
  const refund = await write("settle", [id]);
  console.log(JSON.stringify({ step: "refund_after_nonapproval", ...txSummary(refund), state: await read(id) }));
} else if (reviewed.status === "approved") {
  console.log(JSON.stringify({ step: "approved_waits_for_review_window", timeout_at: reviewed.timeout_at, recovery_at: reviewed.recovery_at }));
}
