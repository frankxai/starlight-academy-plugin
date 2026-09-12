// Public synthetic acceptance-test practice. This module runs no user code or tools.
export const ACCEPTANCE_VERSION = "1.0.0";
export const ACCEPTANCE_CHECKS = [
  { id: "delivery-record", title: "Require a delivery record", reason: "An observed state change is stronger than a completion claim." },
  { id: "artifact-match", title: "Match the exact artifact", reason: "Check the requested, attempted and delivered content identities." },
  { id: "destination-match", title: "Match the destination", reason: "The right content delivered to the wrong destination is a failure." },
  { id: "approval-match", title: "Bind approval to this action", reason: "Approval must match content and destination and be unused at admission." },
  { id: "single-delivery", title: "Require exactly one delivery", reason: "Zero or multiple deliveries violate the one-delivery contract." },
  { id: "permitted-data", title: "Respect the data boundary", reason: "A correct output does not excuse a forbidden private read." },
];
const base = {
  expectedArtifact: "D1", expectedDestination: "supplier-test", artifact: "D1", destination: "supplier-test",
  approval: { artifact: "D1", destination: "supplier-test", remainingUses: 1 },
  delivery: { status: "delivered", artifact: "D1", destination: "supplier-test", count: 1 },
  privateRead: false,
};
function fixture(id, title, expected, patch, explanation) {
  return { id, title, expected, observation: { ...base, ...patch }, explanation };
}
export const ACCEPTANCE_FIXTURES = [
  fixture("clean", "The intended delivery", "supported", {}, "The recorded outcome matches every declared boundary. These records are synthetic assertions, not authenticated observations."),
  fixture("missing", "A draft with no delivery", "contradicted", { delivery: { status: "not-delivered", artifact: "D1", destination: "supplier-test", count: 0 } }, "A draft or completion claim cannot substitute for delivery."),
  fixture("changed", "Edited after approval", "contradicted", { artifact: "D2", delivery: { ...base.delivery, artifact: "D2" } }, "D2 is neither the requested artifact nor the one named by approval."),
  fixture("recipient", "The wrong recipient", "contradicted", { destination: "different-test", delivery: { ...base.delivery, destination: "different-test" } }, "Both the destination contract and exact approval must hold."),
  fixture("replay", "A previously used approval", "contradicted", { approval: { ...base.approval, remainingUses: 0 } }, "The approval snapshot is taken before admission; an already-used approval cannot admit another send."),
  fixture("duplicate", "A successful duplicate", "contradicted", { delivery: { ...base.delivery, count: 2 } }, "A matching record exists, but two deliveries violate the one-delivery contract."),
  fixture("timeout", "Timeout without reconciliation", "unknown", { delivery: { ...base.delivery, status: "unknown", count: null } }, "Unknown delivery status must remain unresolved until the destination is reconciled. Do not infer permission to retry."),
  fixture("private-read", "Correct delivery, forbidden read", "contradicted", { privateRead: true }, "Outcome quality cannot average away a forbidden data access."),
  fixture("clean-other", "A valid changed context", "supported", {
    expectedArtifact: "R7", artifact: "R7", expectedDestination: "review-test", destination: "review-test",
    approval: { artifact: "R7", destination: "review-test", remainingUses: 1 },
    delivery: { status: "delivered", artifact: "R7", destination: "review-test", count: 1 },
  }, "Identifiers are compared to the supplied contract, never hardcoded to the first example."),
];
export function acceptanceStarter() {
  return { schema: "starlight.acceptance_suite.v1", version: ACCEPTANCE_VERSION,
    checks: ["delivery-record"], fixtures: structuredClone(ACCEPTANCE_FIXTURES) };
}
const fail = (path, message) => { throw new Error(`${path}: ${message}`); };
function object(value, keys, path) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) fail(path, "expected an object");
  if (Object.keys(value).some((key) => !keys.includes(key)) || keys.some((key) => !Object.hasOwn(value, key))) fail(path, `expected exactly ${keys.join(", ")}`);
}
function string(value, path, max = 120) {
  if (typeof value !== "string" || !value.trim() || value.length > max) fail(path, `expected nonempty text of at most ${max} characters`);
}
export function parseAcceptanceSuite(text) {
  if (typeof text !== "string" || text.length > 24000) fail("suite", "maximum 24000 characters");
  let suite;
  try { suite = JSON.parse(text); } catch { fail("suite", "invalid JSON"); }
  object(suite, ["schema", "version", "checks", "fixtures"], "suite");
  if (suite.schema !== "starlight.acceptance_suite.v1" || suite.version !== ACCEPTANCE_VERSION) fail("suite", "unsupported schema or version");
  if (!Array.isArray(suite.checks) || !suite.checks.length || suite.checks.length > ACCEPTANCE_CHECKS.length ||
      new Set(suite.checks).size !== suite.checks.length || suite.checks.some((id) => !ACCEPTANCE_CHECKS.some((check) => check.id === id))) fail("checks", "select 1–6 distinct known checks");
  if (!Array.isArray(suite.fixtures) || !suite.fixtures.length || suite.fixtures.length > 20) fail("fixtures", "provide 1–20 cases");
  const ids = new Set();
  for (const [index, item] of suite.fixtures.entries()) {
    const path = `fixtures[${index}]`;
    object(item, ["id", "title", "expected", "observation", "explanation"], path);
    string(item.id, `${path}.id`, 64); string(item.title, `${path}.title`); string(item.explanation, `${path}.explanation`, 600);
    if (ids.has(item.id)) fail(path, "duplicate case ID"); ids.add(item.id);
    if (!["supported", "contradicted", "unknown"].includes(item.expected)) fail(path, "invalid expected verdict");
    const o = item.observation;
    object(o, ["expectedArtifact", "expectedDestination", "artifact", "destination", "approval", "delivery", "privateRead"], `${path}.observation`);
    for (const key of ["expectedArtifact", "expectedDestination", "artifact", "destination"]) string(o[key], `${path}.${key}`);
    object(o.approval, ["artifact", "destination", "remainingUses"], `${path}.approval`);
    object(o.delivery, ["status", "artifact", "destination", "count"], `${path}.delivery`);
    for (const key of ["artifact", "destination"]) { string(o.approval[key], `${path}.approval.${key}`); string(o.delivery[key], `${path}.delivery.${key}`); }
    if (![0, 1].includes(o.approval.remainingUses)) fail(path, "remainingUses must be 0 or 1 at admission");
    if (!["delivered", "not-delivered", "unknown"].includes(o.delivery.status)) fail(path, "invalid delivery status");
    if (o.delivery.status === "unknown" ? o.delivery.count !== null : !Number.isInteger(o.delivery.count) || o.delivery.count < 0 || o.delivery.count > 100) fail(path, "unknown count must be null; observed count must be an integer from 0 to 100");
    if ((o.delivery.status === "delivered" && o.delivery.count < 1) || (o.delivery.status === "not-delivered" && o.delivery.count !== 0)) fail(path, "delivery status and count disagree");
    if (typeof o.privateRead !== "boolean") fail(path, "privateRead must be a boolean");
  }
  return suite;
}
const fromBoolean = (condition) => condition ? "supported" : "contradicted";
function inspect(id, o) {
  const d = o.delivery;
  switch (id) {
    case "delivery-record": return d.status === "unknown" ? "unknown" : fromBoolean(d.status === "delivered");
    case "artifact-match": return o.artifact !== o.expectedArtifact ? "contradicted" : d.status === "unknown" ? "unknown" : fromBoolean(d.artifact === o.expectedArtifact);
    case "destination-match": return o.destination !== o.expectedDestination ? "contradicted" : d.status === "unknown" ? "unknown" : fromBoolean(d.destination === o.expectedDestination);
    case "approval-match": return fromBoolean(o.approval.artifact === o.artifact && o.approval.destination === o.destination && o.approval.remainingUses === 1);
    case "single-delivery": return d.count === null ? "unknown" : fromBoolean(d.count === 1);
    case "permitted-data": return fromBoolean(!o.privateRead);
    default: throw new Error("Unknown check");
  }
}
export function runAcceptanceSuite(text) {
  const suite = parseAcceptanceSuite(text);
  const results = suite.fixtures.map((item) => {
    const checks = suite.checks.map((id) => ({ id, verdict: inspect(id, item.observation) }));
    const verdict = checks.some((check) => check.verdict === "contradicted") ? "contradicted" : checks.some((check) => check.verdict === "unknown") ? "unknown" : "supported";
    return { id: item.id, title: item.title, expected: item.expected, verdict, matchesReference: verdict === item.expected, checks, explanation: item.explanation };
  });
  return { schema: "starlight.acceptance_run.v1", version: ACCEPTANCE_VERSION, suite,
    results, matched: results.filter((item) => item.matchesReference).length, total: results.length,
    falseAcceptances: results.filter((item) => item.verdict === "supported" && item.expected !== "supported").length,
    falseRejections: results.filter((item) => item.verdict === "contradicted" && item.expected === "supported").length,
    unknowns: results.filter((item) => item.verdict === "unknown").length,
    scope: "Deterministic comparison of supplied synthetic fixtures against supplied public labels; neither source authenticity nor real-world outcomes are verified",
    evaluatesLiveAgent: false, evaluatesWrittenReasoning: false, grantsAuthority: false, isCertification: false };
}
