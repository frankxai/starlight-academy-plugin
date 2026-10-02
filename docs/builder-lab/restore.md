# Download to inspectable source

The existing Builder Lab 0.1.4 adds `restore` to scaffold/check/pack. A customer can
verify a publisher-supplied ZIP hash, reopen independently usable source, inspect
the supplied licence and test an update without overwriting prior work. This is
a free supporting capability within the existing lab, not a new product or proof
of paid value.

The [copied plugin guide](../../plugins/starlight-builder-lab/README.md#restore-a-downloaded-package-or-inspect-an-update)
contains the complete command, limits and recovery steps. The updated
[build skill](../../plugins/starlight-builder-lab/skills/build-portable-plugin/SKILL.md)
routes download/update requests through the same helper. Its detailed source is
[package_lab.py](../../plugins/starlight-builder-lab/scripts/package_lab.py).

```text
python -B plugins/starlight-builder-lab/scripts/package_lab.py restore DOWNLOAD.zip NEW_DIRECTORY --sha256 PUBLISHER_SHA256
```

The expected hash must come independently from a trusted release/channel record.
The local archive hash alone establishes byte identity, not publisher identity,
purchase entitlement, legal rights, executable safety or host compatibility.
After restoring, inspect source and notices before using host installation controls.
Restore itself never executes or installs content and never connects accounts.

The serious alternative is manual ZIP extraction followed by inspection. The old
release verifier used Python `extractall` for its known generated example. The new
verifier uses the documented restore CLI. Additional behavior checks exercise
duplicate/case/path conflicts, unsafe names, link/special entries, invalid text,
bad CRCs and excessive expansion before destination creation. The supplied
[Python ZIP documentation](https://docs.python.org/3.10/library/zipfile.html)
calls for prior inspection of untrusted archives. These source checks establish
the bounded workflow; no usability speed, human repair-time or paid advantage is
inferred from them.

Actual replay evidence is retained in [restore-proof.json](restore-proof.json):
restore/repack of the lab and a separately copied, MIT-licensed existing quote
workflow; independent files/notice hashes; preservation of a prior edit; and
local drafting/reopening/export from the restored Node skill. This is a synthetic
local artifact trial. It is not Polar delivery, a new native-host comparison,
outside-user cold use or a claim that any directory has listed these packages.
The previous host/evidence files and commercial gates remain unchanged.

Wrong hash or invalid package stops before output creation. Interrupted writing
preserves the partial new directory with a `.restore-incomplete` marker; check and
pack refuse that marked folder. Keep it intact and retry into a fresh sibling. Pack
and restore retain UTF-8 bytes, including Windows CRLF and CR line endings. Updates restore
alongside older versions, followed by human edit reconciliation. Rollback uses the
preserved prior version. There is no automatic update process, credential migration,
per-run entitlement server, hosted customer inference or support bot.

Limits: stored/DEFLATE ZIPs, 32 MiB archive, 16 MiB expanded content, 512 entries,
1 MiB per file, 12 path components and 240-character entry paths. Files are UTF-8 text under
the existing skills-only layout, with Python and JavaScript/Node source allowed.
The package contract also refuses private-key patterns and personal paths. Windows
and Linux source checks cover Python 3.10 and 3.13; other platforms and Unicode
normalization equivalence remain unverified. Every output ancestor must be ordinary,
so system aliases such as macOS `/var` are refused; choose a canonical local parent.
The code assumes ordinary local directories and cooperating writers; it does not
defend against a privileged process replacing paths during a write or guarantee
power-loss recovery. Temporary validation directories belong to that invocation;
partial requested outputs and prior versions are preserved.

BL-01 two-host/cold-use/Dots acceptance and BL-05 actual seller/rights/terms/native
benefit lifecycle stay pending. No catalog registration, price, account, live
purchase, refund or customer messaging is authorized by a local restore result.
