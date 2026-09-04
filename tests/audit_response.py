"""
Audits a generated tutoring response against the rules in rules.py.

Usage:
    python audit_response.py runs/BST/response.md
    python audit_response.py runs/BST/response.md --json runs/BST/audit_report.json
"""

import argparse
import json
import sys
from pathlib import Path

from rules import run_all_rules


def audit(response_path: Path) -> "list[dict]":
    text = response_path.read_text(encoding="utf-8")
    results = run_all_rules(text)
    return [
        {
            "rule_id": r.rule_id,
            "description": r.description,
            "skill_ref": r.skill_ref,
            "passed": r.passed,
            "detail": r.detail,
        }
        for r in results
    ]


def format_report(topic: str, results: "list[dict]") -> str:
    lines = [f"## Audit report: {topic}", ""]
    passed = sum(1 for r in results if r["passed"])
    lines.append(f"**{passed}/{len(results)} rules passed**")
    lines.append("")
    lines.append("| Rule | Result | Detail |")
    lines.append("|---|---|---|")
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        lines.append(f"| `{r['rule_id']}` ({r['skill_ref']}) | {mark} | {r['detail']} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path, help="Path to a generated response.md")
    parser.add_argument("--json", type=Path, default=None, help="Where to write the JSON report")
    parser.add_argument("--topic", default=None, help="Topic label for the printed report")
    args = parser.parse_args()

    if not args.response.exists():
        sys.stderr.write(f"No such file: {args.response}\n")
        sys.exit(1)

    topic = args.topic or args.response.parent.name
    results = audit(args.response)

    print(format_report(topic, results))

    json_path = args.json or args.response.parent / "audit_report.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
