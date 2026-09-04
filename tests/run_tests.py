"""
Orchestrator: generates + audits a fresh tutoring response for each topic in
TOPICS, then writes one combined summary report.

Usage:
    python run_tests.py
    python run_tests.py --topics BST Queue
"""

import argparse
from datetime import datetime
from pathlib import Path

from audit_response import audit, format_report
from generate_response import generate

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TOPICS = ["BST", "Queue", "Stack"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topics", nargs="+", default=DEFAULT_TOPICS)
    parser.add_argument("--run-id", default=None, help="Subfolder name under tests/runs/ (default: timestamp)")
    args = parser.parse_args()

    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "tests" / "runs" / run_id

    sections = [f"# Test run: {run_id}", "", f"Topics: {', '.join(args.topics)}", ""]
    topic_pass_counts = {}

    for topic in args.topics:
        print(f"\n=== Generating response for '{topic}' ===")
        response_path = run_dir / topic / "response.md"
        generate(topic, response_path)

        print(f"=== Auditing response for '{topic}' ===")
        results = audit(response_path)
        json_path = response_path.parent / "audit_report.json"
        import json
        json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

        report = format_report(topic, results)
        print(report)
        sections.append(report)
        sections.append("")
        topic_pass_counts[topic] = (sum(1 for r in results if r["passed"]), len(results))

    sections.insert(3, "## Summary")
    sections.insert(4, "")
    for topic, (p, total) in topic_pass_counts.items():
        sections.insert(5, f"- {topic}: {p}/{total} rules passed")
    sections.insert(5 + len(topic_pass_counts), "")

    summary_path = ROOT / "reports" / "latest_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"\nCombined summary written to {summary_path}")
    print(f"Raw responses + per-topic JSON reports under {run_dir}")


if __name__ == "__main__":
    main()
