import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { createRecord, inspectRecord, parseRecord, MAX_BYTES } from '../scripts/quest_record.mjs';

const catalog = JSON.parse(readFileSync(new URL('../skills/run-learning-quest/references/quests.json', import.meta.url), 'utf8'));
const cli = fileURLToPath(new URL('../scripts/quest_record.mjs', import.meta.url));
test('all quest prerequisites resolve and the recommended graph is acyclic', () => {
  const ids = new Set(catalog.quests.map(q => q.id));
  assert.equal(ids.size, catalog.quests.length);
  const visit = (id, ancestors = []) => {
    assert.ok(!ancestors.includes(id), 'cyclic learning dependency');
    const quest = catalog.quests.find(q => q.id === id);
    assert.ok(quest);
    for (const dependency of quest.prerequisites) visit(dependency, [...ancestors, id]);
  };
  for (const q of catalog.quests) {
    visit(q.id);
    assert.ok(q.firstAttempt.length > 30 && q.workedExample.length > 100 && q.transfer.length > 30);
    assert.ok(q.checks.length >= 4 && q.boundaries.length >= 1);
    assert.equal(inspectRecord(createRecord(q.id)).phase, 'draft');
  }
  assert.equal(catalog.hostedLms, false);
  assert.equal(catalog.authenticatedAssessment, false);
});

test('presence phases cannot create an assessment or bypass an absent first attempt', () => {
  const r = createRecord('frontier-operator');
  r.transfer = { prompt: 'Changed source', response: 'Re-run the source check.' };
  assert.equal(inspectRecord(r).phase, 'draft');
  r.firstAttempt = 'I chose one worker before knowing the answer.';
  assert.equal(inspectRecord(r).phase, 'attempt-recorded');
  r.artifacts.push({ reference: 'local artifact', revision: 'candidate-1', summary: 'First draft' });
  assert.equal(inspectRecord(r).phase, 'artifact-recorded');
  r.critiques.push('Source B contradicts the conclusion.');
  assert.equal(inspectRecord(r).phase, 'critique-recorded');
  r.revisions.push('Revision 2 preserves that contradiction.');
  assert.equal(inspectRecord(r).phase, 'transfer-recorded');
  for (const flag of Object.values(inspectRecord(r).truth)) assert.equal(flag, false);
  assert.ok(inspectRecord(r).missing.includes('goal'));
});

test('Unicode text and exact first attempt survive inspect roundtrip unchanged', () => {
  const r = createRecord('private-second-brain');
  r.firstAttempt = '  初稿 🧭\nLine two\t';
  r.assistance.push('Worked example requested.');
  const before = JSON.stringify(r);
  const parsed = parseRecord(before);
  assert.equal(parsed.record.firstAttempt, r.firstAttempt);
  assert.equal(JSON.stringify(parsed.record), before);
});

test('reject unknown editions, quest IDs, fields and forged authority', () => {
  const mutants = [null, [], { ...createRecord('agent-canvas'), extra: true },
    { ...createRecord('agent-canvas'), catalogVersion: '9.0.0' },
    { ...createRecord('agent-canvas'), questId: 'other' }];
  for (const k of ['authenticated', 'assessed', 'isCertification', 'grantsAuthority']) {
    const r = createRecord('agent-canvas'); r.truth[k] = true; mutants.push(r);
  }
  for (const r of mutants) assert.equal(inspectRecord(r).valid, false);
  assert.throws(() => createRecord('other'));
});

test('reject malformed nested fields and oversized text or arrays', () => {
  for (const change of [
    { firstAttempt: 'x'.repeat(8001) }, { artifacts: [{ reference: '', revision: '', summary: '' }] },
    { critiques: Array(21).fill('x') }, { transfer: { prompt: '', response: '', score: 100 } },
    { assistance: [true] }, { artifacts: [null] }, { truth: { authenticated: false } },
  ]) assert.equal(inspectRecord({ ...createRecord('product-studio'), ...change }).valid, false);
  const r = createRecord('product-studio');
  r.assistance = Array(20).fill('🧭'.repeat(4000));
  assert.equal(inspectRecord(r).valid, false);
  assert.throws(() => parseRecord(' '.repeat(MAX_BYTES + 1)));
  assert.throws(() => parseRecord(Buffer.from([0xff, 0xfe])));
});

test('input objects with custom prototypes and prototype keys are rejected', () => {
  const r = createRecord('product-studio');
  assert.equal(inspectRecord(Object.assign(Object.create({ grant: true }), r)).valid, false);
  const hostile = JSON.parse(JSON.stringify(r).replace('"goal":""', '"__proto__":{"polluted":true},"goal":""'));
  assert.equal(inspectRecord(hostile).valid, false);
  assert.equal({}.polluted, undefined);
});

test('CLI prints a safe report without echoing learner text and refuses bad input', () => {
  const r = createRecord('frontier-operator'); r.firstAttempt = 'PRIVATE_SENTINEL';
  const result = spawnSync(process.execPath, [cli, 'inspect'], { input: JSON.stringify(r), encoding: 'utf8' });
  assert.equal(result.status, 0);
  assert.equal(result.stdout.includes('PRIVATE_SENTINEL'), false);
  assert.equal(JSON.parse(result.stdout).phase, 'attempt-recorded');
  for (const input of ['{', JSON.stringify({ ...r, authenticated: true }), 'PRIVATE_SENTINEL']) {
    const bad = spawnSync(process.execPath, [cli, 'inspect'], { input, encoding: 'utf8' });
    assert.equal(bad.status, 1); assert.equal(bad.stdout, '');
    assert.equal(bad.stderr.includes('PRIVATE_SENTINEL'), false);
  }
});
