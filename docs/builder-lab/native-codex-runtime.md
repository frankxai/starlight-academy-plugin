# Codex recovery and Windows source access

Builder Lab 0.1.5 fixes a Windows source-access defect found during a controlled
Codex restore-to-quote trial. New folders inherit the chosen workspace parent's
ACL, including nested directories. POSIX folders retain mode `0700`. Choose a
parent restricted to intended collaborators and verify access from the account
that will maintain the package. Restore never changes an existing folder's ACL.

The [JSON record](native-codex-runtime.json) separates the original 0.1.4 failure
from the corrected model-free replay. Private trace hashes identify the retained
evidence; public hashes alone do not let a reviewer inspect those private files.

## Original model attempt

Codex CLI 0.159.3, gpt-6.1-sol/high and existing CPython 3.11.15 observed 19 target
CLI calls: 11 successes and 8 expected refusals. Twelve package calls covered
restore/check/repack and refusal cases. Seven Quote Desk calls covered creation,
intake, authored editing, reopen, selected buyer export and retained-hash
verification, including wrong-hash refusal. Node was 24.16.0.

The 240-second session timed out. Its worker is stopped. No final response,
`turn.completed` or complete native usage/cost receipt exists. Of 28 total command
items, two additional inspection commands failed: an absent fixture directory
and a six-file restored-source read with access denials. The model read the
unchanged producer source and disclosed that assistance in its owner notes.

The maintaining account also could not read either restored source folder.
Its `rglob` returned no files, which was an access failure, not an empty package.
The sandbox ran package checks and produced a byte-identical repack, but ordinary
source inspection/editing was unavailable. Both failed folders remain unchanged.

Original Builder source: `a653f01cd69bbc30aa3394b9a4a3485231cd92ec`. Current MIT Quote Desk:
`8fbd3ae606f256d25a59aeea6a52ac063654ff5c`. Quote manifests are private trial adapters.
Local `.agents` skill discovery was observed through the CLI's actual alias.
No native plugin installation or marketplace registration was performed.

## Corrected source replay

The fix executed at `4412e79a4117a689f2e49f8f7687167cba6a2218` with the same ZIP and
existing interpreter. The sandbox identity was the dedicated offline account.
The ordinary maintaining account read all ten restored files and their notices,
then edited the README. Sandboxed Python separately read and hashed five source
files. A new repack matched the original ZIP exactly before the edit; the edited
repack preserved only that authorized README change. Reusing the edited output
was refused without modifying it. A fresh sibling restored all ten original files.

Eight package calls produced seven successes and one expected existing-output
refusal. The replay also retained identity/read probes and the regression result:
13 model-free process calls overall. Two PowerShell spawn probes failed before
file access: PATH lookup error 2 and explicit Store-executable access error 5.
The subsequent explicit Python read passed. No global runtime or account repair
was attempted. All receipted workers stopped.

The new Windows test checks an inherited read rule at every restored directory.
It fails against the unchanged 0.1.4 runtime. A separate POSIX test checks private
directory permissions. The replay inspected actual nested ACL inheritance from
the maintaining account. These checks cover fresh source access, not every host,
outside-user recovery or a complete native model session.

[Python documents](https://docs.python.org/3.11/library/os.html#os.mkdir) the Windows
creator-only ACL behavior of mode `0o700`, introduced in 3.11.10. The original
restore used that mode for every output directory. The observed cross-account
failure and corrected replay support this fix; they do not explain every denied
runtime on this machine.

## Actual draft retained from the model attempt

The model authored and saved this synthetic buyer wording, separate from owner
notes. A later command reopened revision 2 and exported it. Human scope, price,
tax, timing, prose and rights review remains pending. Outbound actions are disabled.

```text
Thank you for requesting an inspection of one unit at your workshop.

For one equipment inspection visit, the draft amount is EUR 120.00. The scope, final price and tax treatment still need the owner's approval.

You proposed next week. Availability has not yet been confirmed, and no appointment is booked. Please share the equipment type and model, the workshop address and any access requirements, along with your preferred days next week, so the owner can review the scope and timing.

This is a draft for review, not a confirmed booking or binding offer.
```

Quote SHA-256: `9ded0454f2f8fae3b331f8ad6a32e191f05afeabd311ab4613d24810ca8c4354`. The owner retained receipt hash
`c4b45c8f09c9e4afaa8fe1ef13b5bcdcfe66208ab1fa6aee2abe01055d1244a5` outside the buyer folder. The trace contains a read-only verification
against that value and refusal of a wrong value. The lead independently verified
all four buyer files and their payload hashes. Integrity does not approve a quote.

## Remaining acceptance

Python 3.13 still cannot launch inside the tested sandbox, including a correctly
parsed per-invocation read profile. The existing 3.11 executable has a pre-existing
sandbox-user modify ACL; this work neither changed nor certified it. Follow the
[official Windows sandbox guide](https://learn.chatgpt.com/docs/windows/windows-sandbox)
and [support recovery steps](support.md). Global config and protected fixture
bytes were preserved, and the temporary model profile was removed.

This is assisted synthetic use with supplied paths, producer-known hashes and
fictional service facts. Manual extraction, source inspection and copying the
same wording remain capable alternatives; no paid or repair-time advantage was
measured. Native mid-write interruption was not tested. Prior failures remain.

[BL-01](https://github.com/frankxai/starlight-academy-plugin/issues/3) remains
In review with two of four criteria accepted. Completed current-host sessions,
isolated plugin lifecycle, outside-user recovery and Dots evidence remain pending
by 8 October. Actual seller, rights, terms and purchase/refund/revocation/update
evidence remains under [BL-05](https://github.com/frankxai/starlight-academy-plugin/issues/9).
The timed-out model attempt belongs only to BL-01; its total tokens and cost are
unknown. Model-free diagnostics are excluded from model-spend accounting.
