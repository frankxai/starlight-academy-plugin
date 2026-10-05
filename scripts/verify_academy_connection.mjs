#!/usr/bin/env node
// Verify source payload and catalog pin. No host install, networking or commerce.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const plugin = path.join(root, 'plugins', 'starlight-academy');
const json = (file) => JSON.parse(readFileSync(file, 'utf8'));
const manifest = json(path.join(plugin, 'plugin.json'));
const receipt = json(path.join(root, 'docs', 'academy', 'connection-release.json'));
const catalog = json(path.join(root, '.claude-plugin', 'marketplace.json'));
const row = catalog.plugins.find((p) => p.name === manifest.name);
function files(dir, prefix = '') {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    assert.ok(!entry.isSymbolicLink(), 'Package must not contain symlinks');
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    return entry.isDirectory() ? files(path.join(dir, entry.name), relative) : [relative];
  }).sort();
}

try {
  assert.equal(receipt.schema, 'starlight.academy_connection_source.v2');
  assert.equal(receipt.version, manifest.version);
  assert.equal(receipt.plugin, manifest.name);
  assert.match(receipt.payloadRevision, /^[a-f0-9]{40}$/);
  assert.equal(row.source.sha, receipt.payloadRevision);
  assert.equal(row.source.path, 'plugins/starlight-academy');
  assert.equal(row.source.url, 'https://github.com/frankxai/starlight-academy-plugin.git');
  assert.equal(row.version, manifest.version);
  const actual = files(plugin);
  assert.deepEqual(actual, Object.keys(receipt.files).sort());
  const pinnedTree = spawnSync('git', ['ls-tree', '-r', '--name-only', `${receipt.payloadRevision}:plugins/starlight-academy`], { cwd: root, encoding: 'utf8' });
  assert.equal(pinnedTree.status, 0, 'Pinned payload object must be available; use a complete Git checkout');
  assert.deepEqual(pinnedTree.stdout.trim().split('\n').sort(), actual, 'Pinned file inventory differs');
  for (const name of actual) {
    const bytes = readFileSync(path.join(plugin, name));
    assert.equal(createHash('sha256').update(bytes).digest('hex'), receipt.files[name], `Payload changed: ${name}`);
    const pinned = spawnSync('git', ['show', `${receipt.payloadRevision}:plugins/starlight-academy/${name}`], { cwd: root, maxBuffer: 8 * 1024 * 1024 });
    assert.equal(pinned.status, 0, `Pinned source unavailable: ${name}`);
    assert.equal(createHash('sha256').update(pinned.stdout).digest('hex'), receipt.files[name], `Pinned source differs: ${name}`);
  }
  const presentation = manifest.extensions['com.openai'].interface;
  assert.ok(presentation.shortDescription.length <= 30);
  for (const field of ['logo', 'composerIcon']) assert.ok(existsSync(path.join(plugin, presentation[field])));
  const publicMcp = json(path.join(plugin, 'mcp.json')).mcpServers['starlight-academy'];
  const nativeMcp = json(path.join(plugin, '.mcp.json')).mcpServers['starlight-academy'];
  assert.equal(publicMcp.url, 'https://starlightintelligence.academy/mcp');
  assert.equal(publicMcp.type, 'streamable-http');
  assert.equal(nativeMcp.url, publicMcp.url);
  assert.equal(nativeMcp.type, 'http');
  process.stdout.write(`${JSON.stringify({ status: 'connection-source-checks-pass', plugin: manifest.name,
    version: manifest.version, files: actual.length, payloadRevision: receipt.payloadRevision,
    hostBehavior: 'not-proven-by-this-check', entitlement: 'not-checked', deployment: 'not-performed' }, null, 2)}\n`);
} catch (error) {
  process.stderr.write(`Academy connection source check failed: ${error.message}\n`);
  process.exitCode = 1;
}
