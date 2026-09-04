"""
Simulates a "fresh AI" reading iKoott-Assessment-Tutor-Skill.md + the sample
assessment for the very first time, and asks it to produce the full teaching
response for one topic.

"Fresh" here means: a brand-new, stateless `claude -p` process with no memory
of this session or any prior topic. It only ever sees the skill file text +
the assessment text + a one-shot instruction, exactly like a student pasting
those two files into a new chat and asking to be taught.

Usage:
    python generate_response.py BST
    python generate_response.py Queue --out runs/2026-09-04/Queue/response.md
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = ROOT / "iKoott-Assessment-Tutor-Skill.md"
ASSESSMENT_FILE = ROOT / "tests" / "assessment.txt"

PROMPT_TEMPLATE = """You are given a skill file and an assessment description below. Adopt the \
skill file as your complete operating instructions for this reply.

Assume the onboarding steps in the skill file have already happened in this session: the \
welcome message was shown, the assessment overview was given, the student chose English mode, \
the learning path was shown, and the student just confirmed they want to start the topic \
"{topic}" now.

Produce ONLY the full lecture-mode teaching response for the topic "{topic}", from the class \
opening through the class closing, following the skill file's "Core Teaching Structure" and \
"Git Teaching Rules" sections exactly and completely (both Pass 1 and Pass 2, in order, with \
every element they require). Do not summarize or truncate — write it out in full as you would \
actually say it to the student, including all code blocks.

=== SKILL FILE (iKoott-Assessment-Tutor-Skill.md) ===
{skill}

=== ASSESSMENT (extracted from the attached PDF) ===
{assessment}

=== END OF INPUTS ===

Now produce the full lecture-mode teaching response for topic "{topic}".
"""


def generate(topic: str, out_path: Path) -> Path:
    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    assessment_text = ASSESSMENT_FILE.read_text(encoding="utf-8")
    prompt = PROMPT_TEMPLATE.format(topic=topic, skill=skill_text, assessment=assessment_text)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(ROOT),
        timeout=600,
    )

    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"claude -p exited with code {result.returncode}")

    out_path.write_text(result.stdout, encoding="utf-8")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help='Topic to teach, e.g. "BST", "Queue", "Stack"')
    parser.add_argument("--out", type=Path, default=None, help="Output path for the response markdown")
    args = parser.parse_args()

    out_path = args.out or (ROOT / "tests" / "runs" / args.topic / "response.md")
    path = generate(args.topic, out_path)
    print(f"Saved response for '{args.topic}' -> {path}")


if __name__ == "__main__":
    main()
