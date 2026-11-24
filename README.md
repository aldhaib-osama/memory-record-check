# Memory Record Check

AI-security educational prototype for memory-metadata hygiene. Initial code was AI-assisted. It checks required metadata, source/scope combinations, duplicate IDs, timezone-aware timestamps and expiry. It does not read an agent's actual memory or authenticate a user.

```sh
python memory_check.py example.json --at 2026-01-02T12:00:00Z
python -m unittest -v
```

The fictional example returns 1 because an external claim is labeled as a preference. Exit 0 means these metadata checks found no issues, not that a record is trusted. Exit 2 is malformed input. Expiry is inclusive: a record is expired at its expires_at instant. The evaluation time is explicit for reproducibility. All timestamps must include a timezone. Unknown fields/scopes/kinds and duplicate IDs are input errors.

## Trust boundary and limits

source_kind and source_ref are untrusted assertions in this JSON. An attacker can forge user_statement and pass the structural checks. This tool deliberately does not turn a passing record into permission or authority. The test suite includes that limitation. A real application needs authenticated source bindings and an authorized write path outside the record, plus revocation, retrieval controls and human correction. Expiry only works if the consuming system enforces it; this CLI does not delete or modify records. It does not inspect note contents, detect prompt injection, validate signatures, verify source existence or enforce cross-user privacy. It stores no memory body and makes no network calls. Use fictional metadata only in this repository; real source references may reveal private information.

Python 3.9+ is an intended compatibility target. Assistant verification is not Dahoba's personal execution. A prepared workflow is not a completed CI result. See GUIDE_AR.md.

Reference: https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/
