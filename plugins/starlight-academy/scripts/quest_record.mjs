#!/usr/bin/env node
// Offline format inspection only. No storage, network, model calls or assessment.
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const MAX_BYTES = 128 * 1024;
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(readFileSync(path.join(root, 'skills/run-learning-quest/references/quests.json'), 'utf8'));
const flags = { authenticated: false, assessed: false, isCertification: false, grantsAuthority: false };
const fields = ['schema', 'catalogVersion', 'questId', 'goal', 'modelSetup', 'firstAttempt', 'assistance', 'artifacts', 'critiques', 'revisions', 'transfer', 'truth'];
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x) && Object.getPrototypeOf(x) === Object.prototype;
const exact = (x, keys) => object(x) && Object.keys(x).length === keys.length && keys.every(k => Object.hasOwn(x, k));
const text = x => typeof x === 'string' && x.length <= 8000;
const texts = x => Array.isArray(x) && x.length <= 20 && x.every(text);
const questExists = id => catalog.quests.some(q => q.id === id);

export function createRecord(questId) {
  if (!questExists(questId)) throw new Error('Unknown quest ID.');
  return { schema: 'starlight.academy_quest_practice.v1', catalogVersion: catalog.version,
    questId, goal: '', modelSetup: '', firstAttempt: '', assistance: [], artifacts: [],
    critiques: [], revisions: [], transfer: { prompt: '', response: '' }, truth: { ...flags } };
}

export function inspectRecord(record) {
  const fail = code => ({ schema: 'starlight.academy_quest_inspection.v1', valid: false, error: code, truth: { ...flags } });
  if (!exact(record, fields)) return fail('record-fields');
  if (record.schema !== 'starlight.academy_quest_practice.v1' || record.catalogVersion !== catalog.version) return fail('schema-or-edition');
  if (!questExists(record.questId)) return fail('quest-id');
  for (const field of ['goal', 'modelSetup', 'firstAttempt']) if (!text(record[field])) return fail('text-bounds');
  for (const field of ['assistance', 'critiques', 'revisions']) if (!texts(record[field])) return fail('list-bounds');
  if (!Array.isArray(record.artifacts) || record.artifacts.length > 20 || !record.artifacts.every(x => exact(x, ['reference', 'revision', 'summary']) && ['reference', 'revision', 'summary'].every(k => text(x[k]) && x[k].trim()))) return fail('artifact-fields');
  if (!exact(record.transfer, ['prompt', 'response']) || !text(record.transfer.prompt) || !text(record.transfer.response)) return fail('transfer-fields');
  if (!exact(record.truth, Object.keys(flags)) || Object.keys(flags).some(k => record.truth[k] !== false)) return fail('authority-claim');
  if (Buffer.byteLength(JSON.stringify(record), 'utf8') > MAX_BYTES) return fail('record-size');
  const present = { goal: Boolean(record.goal.trim()), modelSetup: Boolean(record.modelSetup.trim()),
    firstAttempt: Boolean(record.firstAttempt.trim()), artifact: record.artifacts.length > 0,
    critique: record.critiques.some(x => x.trim()), revision: record.revisions.some(x => x.trim()),
    transfer: Boolean(record.transfer.prompt.trim() && record.transfer.response.trim()) };
  const phases = ['attempt-recorded', 'artifact-recorded', 'critique-recorded', 'revision-recorded', 'transfer-recorded'];
  const chain = ['firstAttempt', 'artifact', 'critique', 'revision', 'transfer'];
  let phase = 'draft';
  for (let i = 0; i < chain.length && present[chain[i]]; i++) phase = phases[i];
  return { schema: 'starlight.academy_quest_inspection.v1', valid: true, questId: record.questId,
    catalogVersion: record.catalogVersion, phase, missing: Object.keys(present).filter(k => !present[k]),
    meaning: 'Presence and format only; no semantic grading, authenticated review or completion award.', truth: { ...flags } };
}

export function parseRecord(bytes) {
  if (!(typeof bytes === 'string' || Buffer.isBuffer(bytes)) || Buffer.byteLength(bytes, 'utf8') > MAX_BYTES) throw new Error('Record exceeds input limit.');
  const raw = Buffer.isBuffer(bytes) ? new TextDecoder('utf-8', { fatal: true }).decode(bytes) : bytes;
  const record = JSON.parse(raw);
  const report = inspectRecord(record);
  if (!report.valid) throw new Error('Invalid quest record.');
  return { record, report };
}

async function main(args) {
  if (args.length === 2 && args[0] === 'create') return createRecord(args[1]);
  if (args.length !== 1 || args[0] !== 'inspect') throw new Error('Invalid command.');
  const chunks = []; let size = 0;
  for await (const chunk of process.stdin) {
    size += chunk.length;
    if (size > MAX_BYTES) throw new Error('Record exceeds input limit.');
    chunks.push(chunk);
  }
  return parseRecord(Buffer.concat(chunks)).report;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { process.stdout.write(`${JSON.stringify(await main(process.argv.slice(2)), null, 2)}\n`); }
  catch { process.stderr.write('{"status":"refused","reason":"Invalid command or practice record."}\n'); process.exitCode = 1; }
}
