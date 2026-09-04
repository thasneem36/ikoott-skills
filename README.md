# iKoott Assessment Tutor — Skill + Compliance Test Harness

## Contents

- [`iKoott-Assessment-Tutor-Skill.md`](iKoott-Assessment-Tutor-Skill.md) — the skill file itself.
- [`CIT300_Mid_Assignment.pdf`](CIT300_Mid_Assignment.pdf) — sample assessment used to test the skill (Mini Hospital Emergency Management System: BST, Queue, Stack, Linked List).
- `tests/` — a rule-based harness that checks whether a tutoring response generated from the skill file actually follows its own rules.
- `reports/latest_summary.md` — combined output of the most recent test run (generated, not hand-written).

## How the test harness works

1. **Generate** (`tests/generate_response.py`) — spawns a brand-new, stateless `claude -p` process for a given topic (e.g. `BST`). It is handed only the skill file text + the extracted assessment text + a one-shot instruction to teach that topic, exactly like a student pasting both files into a fresh chat. This simulates "a fresh AI reading the skill file" because the subprocess has no memory of this repo, this conversation, or any other topic run.
2. **Audit** (`tests/audit_response.py` + `tests/rules.py`) — parses the generated response and checks it against a fixed set of heuristic rules extracted from specific lines of the skill file (diagram-before-code, inline argument comments, Pass 1 before Pass 2, commit-only-after-full-topic, etc.). Produces a pass/fail table plus a JSON report.
3. **Orchestrate** (`tests/run_tests.py`) — runs steps 1–2 across several topics (default: `BST`, `Queue`, `Stack`) and writes one combined `reports/latest_summary.md`.

Each run's raw response + JSON report is saved under `tests/runs/<run-id>/<topic>/`.

### Running it

```bash
python tests/run_tests.py
python tests/run_tests.py --topics BST Queue Stack
```

Each topic run spawns a real `claude -p` call and consumes API/usage — it is not free or instant. Nothing runs automatically; you trigger it explicitly.

### Limitations — read before trusting a PASS

These are **regex/structural heuristics**, not semantic understanding. A rule can:
- **False-pass**: e.g. `inline_arg_comments` only checks that a `//` appears on the signature line, not that the comment is actually correct or per-argument.
- **False-fail**: e.g. `diagram_before_code` looks for arrow/box characters or the word "diagram" — a valid prose-only diagram description could be missed.

Treat FAILs as "worth a human look," and PASSes as "no obvious mechanical violation" — not a substitute for actually reading the response.

## Workflow for skill-file changes

1. Run the harness, review `reports/latest_summary.md`.
2. For any FAIL, a diff against `iKoott-Assessment-Tutor-Skill.md` is proposed in chat — never auto-applied.
3. Only after explicit approval is the skill file edited and committed, with a commit message describing which rule/behavior the change addresses.
