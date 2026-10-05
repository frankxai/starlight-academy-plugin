import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { prepareHandoff } from '../scripts/architect_handoff.mjs';

const plugin = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('human and agent lanes prepare separate records without granting access', () => {
  for (const lane of ['human', 'agent']) {
    const plan = prepareHandoff({ origin: 'https://academy.example/', lane });
    assert.equal(plan.academy.entry, `https://academy.example/start#${lane}`);
    assert.equal(plan.academy.discovery, 'https://academy.example/.well-known/academy.json');
    assert.equal(plan.connections.starlight.url, 'https://starlightintelligence.academy/mcp');
    assert.equal(plan.connections.architectMcp, null);
    assert.equal(plan.status, 'prepared-not-installed');
    assert.equal(plan.connections.privateResources.entitlement, 'not-checked');
    for (const flag of ['grantsAuthority', 'provesEntitlement', 'verifiesArchitecture', 'installed']) assert.equal(plan[flag], false);
    assert.equal(plan.record.sponsor, lane === 'agent' ? 'name-human-sponsor-in-local-record' : null);
  }
});

test('reject credential-bearing, insecure and non-origin URLs and invalid lanes', () => {
  for (const origin of [undefined, 'http://academy.example', 'https://user:secret@academy.example', 'https://academy.example/path', 'https://academy.example?token=secret', 'https://academy.example/#secret', 'https://academy.example ']) {
    assert.throws(() => prepareHandoff({ origin }));
  }
  assert.throws(() => prepareHandoff({ origin: 'https://academy.example', lane: 'administrator' }));
});

test('local source identity is inspected without executing code or changing bytes', () => {
  const root = mkdtempSync(path.join(os.tmpdir(), 'architect-handoff-'));
  try {
    mkdirSync(path.join(root, 'mcp'));
    const marker = 'throw new Error("must never execute source");\n';
    writeFileSync(path.join(root, 'mcp', 'server.mjs'), marker);
    writeFileSync(path.join(root, 'package.json'), JSON.stringify({ name: '@frankxai/ai-architect', version: '0.1.3', license: 'Apache-2.0' }));
    const plan = prepareHandoff({ origin: 'https://academy.example', lane: 'agent', architectRoot: root });
    assert.equal(plan.connections.architectMcp.mcpServers['ai-architect'].args[0], path.join(root, 'mcp', 'server.mjs'));
    assert.equal(plan.architect.local.license, 'Apache-2.0');
    assert.equal(readFileSync(path.join(root, 'mcp', 'server.mjs'), 'utf8'), marker);
    writeFileSync(path.join(root, 'package.json'), '{"name":"another-package"}');
    assert.throws(() => prepareHandoff({ origin: 'https://academy.example', architectRoot: root }));
  } finally { rmSync(root, { recursive: true, force: true }); }
  assert.throws(() => prepareHandoff({ origin: 'https://academy.example', architectRoot: 'relative-path' }));
});

test('CLI has JSON success and refuses malformed flags without exposing input secrets', () => {
  const script = path.join(plugin, 'scripts', 'architect_handoff.mjs');
  const good = spawnSync(process.execPath, [script, '--academy-origin', 'https://academy.example', '--lane', 'agent'], { encoding: 'utf8' });
  assert.equal(good.status, 0);
  assert.equal(JSON.parse(good.stdout).schema, 'starlight.architect_handoff.v1');
  for (const args of [[], ['--academy-origin', 'https://user:secret@academy.example'], ['--academy-origin', 'https://academy.example', '--lane'], ['--academy-origin', 'https://academy.example', '--lane', 'agent', '--lane', 'human'], ['--academy-origin', 'https://academy.example', '--unknown', 'secret']]) {
    const refused = spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });
    assert.equal(refused.status, 1);
    assert.equal(refused.stdout, '');
    assert.equal(JSON.parse(refused.stderr).status, 'refused');
    assert.equal(refused.stderr.includes('secret'), false);
  }
});

test('portable and native package identities, presentation and prompts match', () => {
  const portable = JSON.parse(readFileSync(path.join(plugin, 'plugin.json'), 'utf8'));
  const codex = JSON.parse(readFileSync(path.join(plugin, '.codex-plugin', 'plugin.json'), 'utf8'));
  const claude = JSON.parse(readFileSync(path.join(plugin, '.claude-plugin', 'plugin.json'), 'utf8'));
  for (const native of [codex, claude]) {
    for (const key of ['name', 'version', 'description', 'license', 'repository']) assert.equal(native[key], portable[key]);
  }
  assert.deepEqual(codex.interface, portable.extensions['com.openai'].interface);
  assert.ok(codex.interface.shortDescription.length <= 30);
  assert.deepEqual(codex.interface.defaultPrompt, [
    'Help me choose a Starlight Academy challenge.',
    'Guide my first attempt before showing a solution.',
    'Help me give useful feedback when AI gets something wrong.',
  ]);
});
