#!/usr/bin/env python3
"""Offline skills-only scaffolding, checks, text ZIPs and checksum-bound restoration.

Standard library only. No installation, network, credential or commerce actions.
The checks are a bounded project contract, not a provider certification.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import zipfile

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul", "conin$", "conout$",
                    *(f"com{i}" for i in "123456789¹²³"), *(f"lpt{i}" for i in "123456789¹²³")}
DENIED_PARTS = {".git", "node_modules", "__pycache__", ".venv", ".env"}
ROOT_FILES = {"plugin.json", "README.md", "LICENSE", "NOTICE"}
ROOT_DIRS = {"skills", "scripts", "references", "examples", "tests", "LICENSES", ".claude-plugin"}
SECRET = re.compile(r"-----BEGIN (?:(?:[A-Z][A-Z0-9 ]* )?PRIVATE KEY|PGP PRIVATE KEY BLOCK)-----|\b(?:sk-(?:proj-|ant-)?|polar_oat_|sk_live_|whsec_|ghp_|github_pat_)[A-Za-z0-9_-]{24,}|\bAKIA[0-9A-Z]{16}\b")
LOCAL_PATH = re.compile(r"(?<![A-Za-z0-9/:])(?:[A-Za-z]:[/\\]+Users|/Users|/home)[/\\]+[A-Za-z0-9_.-]+[/\\]+")
MAX_ARCHIVE = 32 * 1024 * 1024
MAX_RESTORED = 16 * 1024 * 1024
MAX_MEMBER = 1024 * 1024
MAX_ENTRIES = 512


def indirect(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def ordinary_parents(path: Path) -> None:
    for parent in (path, *path.parents):
        if indirect(parent) or not parent.is_dir():
            raise ValueError("Use an ordinary fully local output parent without links or reparse points")


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    return data


def text_field(data: dict, key: str, limit: int = 4000) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{key} must be nonempty text, at most {limit} characters")
    return value


def slug(value: object) -> str:
    if not isinstance(value, str) or len(value) > 64 or not SLUG.fullmatch(value) or value in WINDOWS_RESERVED:
        raise ValueError("Names must be kebab-case, at most 64 characters")
    return value


def portable_component(value: str) -> None:
    # Names must remain single ordinary components in Windows extractors,
    # even when the package was authored on POSIX.
    if (not value or value in {".", ".."} or value.endswith((".", " "))
            or re.search(r'[<>:"/\\|?*\x00-\x1f]', value)
            or value.split(".", 1)[0].rstrip(' ').lower() in WINDOWS_RESERVED):
        raise ValueError("Unsafe cross-platform package filename")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def scaffold(spec: dict, target: Path) -> dict:
    name = slug(spec.get("name"))
    version = text_field(spec, "version", 30)
    if not VERSION.fullmatch(version):
        raise ValueError("version must be X.Y.Z")
    description = text_field(spec, "description", 1024)
    author = text_field(spec, "author", 120)
    license_id = text_field(spec, "license", 100)
    license_text = text_field(spec, "license_text", 50000)
    rows = spec.get("skills")
    if not isinstance(rows, list) or not rows:
        raise ValueError("At least one skill is required")
    names = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each skill must be an object")
        skill_name = slug(row.get("name"))
        if skill_name in names:
            raise ValueError("Duplicate skill name")
        names.add(skill_name)
        text_field(row, "description", 1024)
        text_field(row, "instructions", 30000)
    # Validate all supplied content before creating any directory.
    supplied_text = [description, author, license_id, license_text]
    supplied_text.extend(value for row in rows for value in (row["description"], row["instructions"]))
    if any(SECRET.search(value) or LOCAL_PATH.search(value) for value in supplied_text):
        raise ValueError("Specification contains a private key pattern or personal path")
    if target.exists() or target.is_symlink():
        raise ValueError("Output directory already exists; existing work is preserved")
    if not target.parent.is_dir():
        raise ValueError("Output parent must already exist in the chosen workspace")
    target.mkdir()
    manifest = {"$schema": SCHEMA, "name": name, "version": version,
                "description": description, "author": {"name": author}, "license": license_id}
    write_json(target / "plugin.json", manifest)
    (target / ".claude-plugin").mkdir()
    write_json(target / ".claude-plugin/plugin.json", {key: value for key, value in manifest.items() if key != "$schema"})
    for row in rows:
        folder = target / "skills" / row["name"]
        folder.mkdir(parents=True)
        body = (f"---\nname: {row['name']}\ndescription: "
                f"{json.dumps(row['description'], ensure_ascii=False)}\n---\n\n"
                f"{row['instructions'].strip()}\n")
        (folder / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
    (target / "LICENSE").write_text(license_text + "\n", encoding="utf-8", newline="\n")
    (target / "README.md").write_text(
        f"# {name}\n\n{description}\n\nVersion: {version}. License: {license_id}.\n\n"
        "Skills-only source package. Validate, inspect and test in your intended host before use.\n"
        "No host tests, directory approval or commercial release are implied by generation.\n",
        encoding="utf-8", newline="\n")
    return {"directory": str(target), "skills": len(rows), "status": "generated-unverified"}


def package_files(root: Path) -> list[Path]:
    if indirect(root) or not root.is_dir():
        raise ValueError("Package must be a real directory")
    files = []
    paths = []
    pending = [root]
    while pending:
        folder = pending.pop()
        sibling_names = set()
        with os.scandir(folder) as entries:
            for entry in entries:
                path = Path(entry.path)
                rel = path.relative_to(root)
                for component in rel.parts:
                    portable_component(component)
                folded = entry.name.casefold()
                if folded in sibling_names:
                    raise ValueError(f"Case-insensitive sibling collision: {rel.as_posix()}")
                sibling_names.add(folded)
                if indirect(path):
                    raise ValueError(f"Symlink or reparse point: {rel.as_posix()}")
                if not entry.is_dir(follow_symlinks=False) and not entry.is_file(follow_symlinks=False):
                    raise ValueError(f"Unsupported special file: {rel.as_posix()}")
                if any(part.lower() in DENIED_PARTS or part.lower().startswith(".env.") for part in rel.parts):
                    raise ValueError(f"Forbidden package path: {rel.as_posix()}")
                if len(rel.parts) == 1 and entry.is_dir(follow_symlinks=False) and rel.name not in ROOT_DIRS:
                    raise ValueError(f"Unexpected package content: {rel.as_posix()}")
                paths.append(path)
                if entry.is_dir(follow_symlinks=False):
                    pending.append(path)
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root)
        if path.is_symlink():
            raise ValueError(f"Symlinks are not package content: {rel.as_posix()}")
        if any(part.lower() in DENIED_PARTS or part.lower().startswith(".env.") for part in rel.parts):
            raise ValueError(f"Forbidden package path: {rel.as_posix()}")
        if (len(rel.parts) == 1 and path.is_file() and rel.name not in ROOT_FILES) or (path.is_dir() and len(rel.parts) == 1 and rel.name not in ROOT_DIRS):
            raise ValueError(f"Unexpected package content: {rel.as_posix()}")
        if path.is_file():
            if path.suffix.lower() not in {".md", ".json", ".py", ".js", ".mjs", ".txt"} and path.name not in {"LICENSE", "NOTICE"}:
                raise ValueError(f"Unsupported file type: {rel.as_posix()}")
            if path.stat().st_size > 1024 * 1024:
                raise ValueError(f"File exceeds this lab's 1 MiB limit: {rel.as_posix()}")
            content = path.read_text(encoding="utf-8")
            if SECRET.search(content) or LOCAL_PATH.search(content):
                raise ValueError(f"Private key pattern or personal path: {rel.as_posix()}")
            files.append(path)
    return files


def check(root: Path) -> dict:
    files = package_files(root)
    manifest = read_json(root / "plugin.json")
    slug(manifest.get("name"))
    if manifest.get("$schema") != SCHEMA or not VERSION.fullmatch(text_field(manifest, "version", 30)):
        raise ValueError("Unsupported manifest schema or version")
    text_field(manifest, "description", 1024)
    text_field(manifest, "license", 100)
    author = manifest.get("author")
    if not isinstance(author, dict):
        raise ValueError("author must be an object")
    text_field(author, "name", 120)
    for filename in ("README.md", "LICENSE"):
        if not (root / filename).is_file() or not (root / filename).read_text(encoding="utf-8").strip():
            raise ValueError(f"Missing or empty {filename}")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills or len(list(root.rglob("SKILL.md"))) != len(skills):
        raise ValueError("Skills must use skills/<name>/SKILL.md without nested skills")
    for path in skills:
        content = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n+(.*)\Z", content, re.S)
        if not match:
            raise ValueError(f"Invalid skill frontmatter: {path.relative_to(root)}")
        fields = {}
        for line in match[1].splitlines():
            item = re.match(r"^(name|description):\s*(.*)$", line)
            if not item:
                continue
            key, value = item.groups()
            if key in fields:
                raise ValueError(f"Duplicate frontmatter field {key}")
            if value.startswith(('>', '|')):
                raise ValueError("Multiline frontmatter requires a full YAML validator; this checker accepts one-line fields")
            if value.startswith('"'):
                value = json.loads(value)
            elif value.startswith("'"):
                if not value.endswith("'"):
                    raise ValueError("Unclosed frontmatter quote")
                value = value[1:-1].replace("''", "'")
            fields[key] = value
        if slug(fields.get("name")) != path.parent.name:
            raise ValueError("Skill name must match its directory")
        text_field(fields, "description", 1024)
        if not match[2].strip():
            raise ValueError("Empty skill instructions")
    compat = root / ".claude-plugin/plugin.json"
    if compat.exists():
        other = read_json(compat)
        for field in ("name", "version", "description", "license"):
            if other.get(field) != manifest.get(field):
                raise ValueError(f"Claude manifest {field} drift")
        native_author = other.get('author')
        if not isinstance(native_author, dict) or native_author.get('name') != author['name']:
            raise ValueError('Claude manifest author identity drift')
        if native_author.get('url') is not None and native_author['url'] != author.get('url'):
            raise ValueError('Claude manifest author URL drift')
    return {"status": "structural-pass", "name": manifest["name"], "skills": len(skills),
            "files": len(files), "hostTests": "not-run", "directoryApproval": "not-submitted",
            "commercialRelease": "not-evaluated", "secretScan": "heuristic-only"}


def pack(root: Path, output: Path) -> dict:
    result = check(root)
    root_resolved, output_resolved = root.resolve(), output.resolve()
    if output_resolved == root_resolved or root_resolved in output_resolved.parents:
        raise ValueError("ZIP must be outside the source package")
    if output.suffix.lower() != ".zip" or output.exists() or output.is_symlink():
        raise ValueError("Use a new .zip path; existing files are preserved")
    files = package_files(root)
    created = False
    try:
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_STORED) as archive:
            created = True
            for path in files:
                info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.compress_type = zipfile.ZIP_STORED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_text(encoding="utf-8").encode("utf-8"))
    except Exception:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {**result, "zip": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def restore(source: Path, output: Path, expected_sha256: str) -> dict:
    """Restore checked bytes into a new folder; never install or execute them."""
    if not isinstance(expected_sha256, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected_sha256):
        raise ValueError("Supply the publisher's independently obtained 64-character SHA-256")
    if indirect(source) or not source.is_file() or source.stat().st_size > MAX_ARCHIVE:
        raise ValueError("ZIP must be an ordinary local file of at most 32 MiB")
    output = Path(os.path.abspath(output))
    ordinary_parents(output.parent)
    portable_component(output.name)
    if os.path.lexists(output):
        raise ValueError("Output directory already exists; existing versions and edits are preserved")
    # Hash and parse the same bounded immutable in-memory bytes, not a reread path.
    with source.open("rb") as stream:
        raw = stream.read(MAX_ARCHIVE + 1)
    if len(raw) > MAX_ARCHIVE:
        raise ValueError("ZIP exceeds 32 MiB; input may have changed")
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha256.lower():
        raise ValueError("ZIP checksum mismatch; preserve the download and obtain the correct release")
    payload, directories, prefixes, seen = {}, set(), {}, set()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        if not entries or len(entries) > MAX_ENTRIES or sum(entry.file_size for entry in entries) > MAX_RESTORED:
            raise ValueError("ZIP must have 1-512 entries and at most 16 MiB of uncompressed content")
        for entry in entries:
            name = entry.filename
            if entry.orig_filename != name or len(name) > 240:
                raise ValueError("ZIP entry has a truncated or oversized name")
            is_directory = entry.is_dir()
            parts = name[:-1].split("/") if is_directory else name.split("/")
            if len(parts) > 12:
                raise ValueError("ZIP entry exceeds the 12-component path limit")
            for part in parts:
                portable_component(part)
            canonical = "/".join(parts)
            if canonical.casefold() in seen:
                raise ValueError("Duplicate or case-colliding ZIP entry")
            seen.add(canonical.casefold())
            for index in range(1, len(parts) + 1):
                prefix = "/".join(parts[:index])
                kind = "directory" if index < len(parts) or is_directory else "file"
                previous = prefixes.setdefault(prefix.casefold(), (prefix, kind))
                if previous != (prefix, kind):
                    raise ValueError("ZIP has a case collision or file/directory conflict")
                if kind == "directory":
                    directories.add(prefix)
            mode = stat.S_IFMT(entry.external_attr >> 16)
            if mode not in (0, stat.S_IFDIR if is_directory else stat.S_IFREG) or entry.external_attr & 0x400:
                raise ValueError("ZIP links, reparse points and special files are unsupported")
            if entry.flag_bits & 1 or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                raise ValueError("Encrypted or unsupported-compression ZIP entries are refused")
            if entry.file_size > MAX_MEMBER or (is_directory and entry.file_size != 0):
                raise ValueError("ZIP member exceeds 1 MiB or directory carries content")
            if not is_directory:
                with archive.open(entry) as stream:
                    content = stream.read(MAX_MEMBER + 1)
                if len(content) != entry.file_size or len(content) > MAX_MEMBER:
                    raise ValueError("ZIP member length differs from its bounded declaration")
                content.decode("utf-8", errors="strict")
                payload[canonical] = content
    # Validate the full package contract before creating the requested output.
    # Only this session's TemporaryDirectory is cleaned; partial customer output is kept.
    with tempfile.TemporaryDirectory(prefix="builder-restore-check-") as temporary:
        stage = Path(temporary)
        for name in sorted(directories, key=lambda value: (value.count("/"), value)):
            (stage / name).mkdir()
        for name, content in payload.items():
            (stage / name).write_bytes(content)
        result = check(stage)
    ordinary_parents(output.parent)
    output.mkdir(mode=0o700)  # Exclusive on every supported OS, even for an empty existing directory.
    try:
        for name in sorted(directories, key=lambda value: (value.count("/"), value)):
            (output / name).mkdir(mode=0o700)
        for name, content in payload.items():
            with (output / name).open("xb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
    except OSError as exc:
        raise ValueError(f"Restore write failed; preserve the partial directory and retry into a fresh sibling. {exc}") from exc
    return {**result, "status": "restored-structural-pass", "directory": str(output),
            "archive_sha256": actual, "files_sha256": {name: hashlib.sha256(content).hexdigest() for name, content in sorted(payload.items())},
            "bytes_restored": sum(map(len, payload.values())), "installation": "not-performed",
            "publisherIdentity": "not-verified-by-checksum", "priorVersions": "not-modified"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("scaffold", "pack"):
        action = sub.add_parser(command)
        action.add_argument("source", type=Path)
        action.add_argument("output", type=Path)
    for command in ("check",):
        sub.add_parser(command).add_argument("source", type=Path)
    action = sub.add_parser("restore")
    action.add_argument("source", type=Path)
    action.add_argument("output", type=Path)
    action.add_argument("--sha256", required=True)
    args = parser.parse_args()
    try:
        if args.command == "scaffold":
            result = scaffold(read_json(args.source), args.output)
        elif args.command == "pack":
            result = pack(args.source, args.output)
        elif args.command == "check":
            result = check(args.source)
        elif args.command == "restore":
            result = restore(args.source, args.output, args.sha256)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
