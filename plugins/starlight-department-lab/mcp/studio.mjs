import missions from "./studio-missions.json" with { type: "json" };

function deepFreeze(value) {
  if (value && typeof value === "object") { for (const item of Object.values(value)) deepFreeze(item); Object.freeze(value); }
  return value;
}
export const STUDIO_MISSIONS = deepFreeze(missions);
export class PracticeCompatibilityError extends Error {}
export const STUDIO_PHASES = ["orient", "attempt", "study", "build", "critique", "reflect", "transfer"];
export const STUDIO_MAX_BYTES = 96 * 1024;
export const STUDIO_TEXT_LIMIT = 16000;
export const STUDIO_ARTIFACT_LIMIT = 24000;
const truth = { assessed: false, authenticated: false, grantsAuthority: false, isCertification: false };
const modes = ["undeclared", "none", "primary-sources", "bounded-hints", "peer-or-agent-critique", "other"];
const bytes = (text) => new TextEncoder().encode(text).length;
const equal = (a, b) => Object.keys(a).length === Object.keys(b).length && Object.keys(a).every((key) => a[key] === b[key]);
const present = (text) => text.trim().length > 0;
function fail(message) { throw new Error(message); }
function object(value, keys, label) {
  if (!value || typeof value !== "object" || Array.isArray(value) || Object.keys(value).length !== keys.length || keys.some((key) => !Object.hasOwn(value, key))) fail(`${label}: unexpected or missing fields.`);
}
function string(value, label, limit = STUDIO_TEXT_LIMIT) {
  if (typeof value !== "string" || value.length > limit) fail(`${label}: expected text of at most ${limit} UTF-16 code units.`);
}
function phase(value, label) {
  object(value, ["text", "assistance", "accommodations"], label);
  string(value.text, label); string(value.accommodations, `${label} accommodations`, 1000);
  if (!modes.includes(value.assistance)) fail(`${label}: unknown assistance declaration.`);
}
function learner(value) {
  object(value, ["kind", "sponsor", "runtime"], "Learner");
  if (!["human", "agent"].includes(value.kind)) fail("Choose a human or agent learner.");
  string(value.sponsor, "Sponsor", 160); string(value.runtime, "Runtime", 160);
  if (value.kind === "human" && (value.sponsor || value.runtime)) fail("Human practice cannot carry agent attribution.");
}
export function getStudioMission(id) {
  const mission = missions.find((item) => item.packet.id === id);
  if (!mission) throw new PracticeCompatibilityError("This mission is not bundled with this Studio. You can read the saved JSON here, but resuming requires its exact mission contract.");
  return structuredClone(mission);
}
export function createPractice(id) {
  const mission = getStudioMission(id);
  return {
    schema: "starlight.mission_practice.v1",
    mission: { id, version: mission.packet.version, digest: mission.digest },
    learner: { kind: "human", sponsor: "", runtime: "" },
    fields: Object.fromEntries(STUDIO_PHASES.map((key) => [key, { text: "", assistance: "undeclared", accommodations: "" }])),
    artifact: "", firstAttempt: null, critiques: [], critiqueReviewer: "", activeStage: "orient", transferContext: "", starterUsed: false, truth: { ...truth },
  };
}
export function parsePractice(input) {
  if (typeof input !== "string" || bytes(input) > STUDIO_MAX_BYTES) fail("Practice file must be UTF-8 JSON no larger than 96 KiB. Keep your original file.");
  let value;
  try { value = JSON.parse(input); } catch { fail("This file is not valid JSON. Keep the original and choose a Mission Studio export."); }
  object(value, ["schema", "mission", "learner", "fields", "artifact", "firstAttempt", "critiques", "critiqueReviewer", "activeStage", "transferContext", "starterUsed", "truth"], "Practice record");
  if (value.schema !== "starlight.mission_practice.v1") fail("This is not a supported Mission Studio practice export.");
  object(value.mission, ["id", "version", "digest"], "Mission");
  string(value.mission.id, "Mission ID", 100); string(value.mission.version, "Mission version", 80);
  if (typeof value.mission.digest !== "string" || !/^[a-f0-9]{64}$/.test(value.mission.digest)) fail("Mission digest must be a 64-character lowercase SHA-256 value.");
  const mission = getStudioMission(value.mission.id);
  if (value.mission.version !== mission.packet.version || value.mission.digest !== mission.digest) throw new PracticeCompatibilityError("Mission version or source digest differs. Open the saved JSON in the Studio reader; resuming it requires the original contract or an explicit migration.");
  learner(value.learner);
  object(value.fields, STUDIO_PHASES, "Practice stages");
  for (const key of STUDIO_PHASES) phase(value.fields[key], key);
  string(value.artifact, "Artifact", STUDIO_ARTIFACT_LIMIT); string(value.transferContext, "Transfer context");
  string(value.critiqueReviewer, "Draft reviewer", 160);
  if (!STUDIO_PHASES.includes(value.activeStage)) fail("Unknown active practice stage.");
  if (typeof value.starterUsed !== "boolean") fail("Starter declaration must be true or false.");
  object(value.truth, Object.keys(truth), "Truth flags");
  for (const key of Object.keys(truth)) if (value.truth[key] !== false) fail("Practice cannot claim assessment, authentication, certification or authority.");
  if (value.firstAttempt !== null) {
    object(value.firstAttempt, ["context", "learner", "response"], "Preserved first attempt");
    string(value.firstAttempt.context, "Initial context"); learner(value.firstAttempt.learner); phase(value.firstAttempt.response, "Initial response");
    if (!present(value.firstAttempt.context) || !present(value.firstAttempt.response.text) || value.firstAttempt.response.assistance === "undeclared") fail("Preserved attempt needs context, a response and an assistance declaration.");
    if (!equal(value.firstAttempt.learner, value.learner) || value.firstAttempt.context !== value.fields.orient.text || !equal(value.firstAttempt.response, value.fields.attempt)) fail("Initial context, learner and response must match the preserved first attempt.");
    if (value.learner.kind === "agent" && !present(value.learner.runtime)) fail("An agent attempt needs its runtime named. Sponsorship remains self-reported and optional for private practice.");
  }
  if (!Array.isArray(value.critiques) || value.critiques.length > 8) fail("Keep at most eight critique snapshots in one record.");
  for (const item of value.critiques) {
    object(item, ["artifact", "reviewer", "response"], "Critique snapshot");
    string(item.artifact, "Reviewed artifact", STUDIO_ARTIFACT_LIMIT); string(item.reviewer, "Reviewer", 160); phase(item.response, "Critique response");
    if (!value.firstAttempt || !present(item.artifact) || !present(item.reviewer) || !present(item.response.text) || item.response.assistance === "undeclared") fail("A critique snapshot needs a first attempt, exact artifact, named reviewer, critique and assistance declaration.");
  }
  if (bytes(JSON.stringify(value, null, 2) + "\n") > STUDIO_MAX_BYTES) fail("This record exceeds the 96 KiB export limit. Keep the previous save and shorten the current draft.");
  return value;
}
export function exportPractice(record) {
  const json = JSON.stringify(record, null, 2) + "\n";
  parsePractice(json);
  return json;
}
export function updatePractice(record, patch) {
  // Only named editable fields. Callers cannot rewrite snapshots or truth flags.
  const editable = ["learner", "fields", "artifact", "transferContext", "critiqueReviewer", "activeStage"];
  if (!patch || Object.keys(patch).some((key) => !editable.includes(key))) fail("This change cannot rewrite preserved practice history.");
  return parsePractice(JSON.stringify({ ...record, ...patch }));
}
export function preserveAttempt(record) {
  if (record.firstAttempt) fail("The first attempt is already preserved. Export it before starting another record.");
  return parsePractice(JSON.stringify({ ...record, firstAttempt: { context: record.fields.orient.text, learner: record.learner, response: record.fields.attempt } }));
}
export function addStudioStarter(record) {
  if (!record.firstAttempt) fail("Preserve your first attempt before using the starter.");
  if (present(record.artifact)) fail("The artifact already has work. The starter cannot overwrite it.");
  return parsePractice(JSON.stringify({ ...record, artifact: getStudioMission(record.mission.id).starter, starterUsed: true }));
}
export function preserveCritique(record, reviewer) {
  if (record.critiques.some((item) => item.artifact === record.artifact && equal(item.response, record.fields.critique) && item.reviewer === reviewer)) fail("This exact critique is already preserved.");
  try { return parsePractice(JSON.stringify({ ...record, critiques: [...record.critiques, { artifact: record.artifact, reviewer, response: record.fields.critique }] })); }
  catch (error) {
    if (error.message.includes("96 KiB")) fail("This critique does not fit beside the preserved history. Download the current practice and keep the new review separately; shortening the reviewed artifact would change the review target.");
    throw error;
  }
}
export function inspectPractice(input) {
  const record = parsePractice(typeof input === "string" ? input : JSON.stringify(input));
  const last = record.critiques.at(-1);
  const starter = getStudioMission(record.mission.id).starter;
  const artifactIsUnmodifiedStarter = record.artifact.replace(/\r\n/g, "\n").trim() === starter.trim();
  let artifactFormat = "No artifact yet";
  let artifactDownloadable = present(record.artifact);
  if (artifactDownloadable && getStudioMission(record.mission.id).packet.artifact.filename.endsWith(".json")) {
    try { JSON.parse(record.artifact); artifactFormat = "JSON parses; contract and quality are unchecked"; }
    catch { artifactFormat = "Artifact JSON needs a syntax correction"; artifactDownloadable = false; }
  } else if (artifactDownloadable) artifactFormat = "Plain Markdown; content quality is unchecked";
  if (artifactIsUnmodifiedStarter) artifactFormat = "Unchanged starter structure; add your own work before review";
  const checks = [
    ["orient", "Context named", present(record.fields.orient.text)],
    ["attempt", "First attempt preserved", record.firstAttempt !== null],
    ["study", "Source notes recorded", present(record.fields.study.text)],
    ["build", "Artifact drafted", present(record.artifact) && !artifactIsUnmodifiedStarter],
    ["critique", "Critique snapshot preserved", !!last],
    ["revision", "Artifact changed since critique", !!last && last.artifact !== record.artifact],
    ["reflect", "Reflection recorded", present(record.fields.reflect.text)],
    ["transfer", "Second context and response recorded", present(record.transferContext) && present(record.fields.transfer.text) && record.transferContext.trim() !== record.fields.orient.text.trim()],
  ].map(([id, label, recorded]) => ({ id, label, recorded }));
  return { schema: "starlight.mission_practice_inspection.v1", mission: record.mission, checks,
    scope: "Presence and format only. No correctness, learning, chronology, sponsorship or authorship is verified.",
    artifactFormat, artifactDownloadable, starterUsed: record.starterUsed, artifactIsUnmodifiedStarter,
    transferRepeatsInitialContext: present(record.transferContext) && record.transferContext.trim() === record.fields.orient.text.trim(),
    critiqueAppliesToCurrentText: !!last && last.artifact === record.artifact,
    transferPending: !checks.at(-1).recorded, bytes: bytes(exportPractice(record)), ...truth };
}
