"""
Rule definitions for auditing an iKoott Tutor response against
iKoott-Assessment-Tutor-Skill.md.

Each rule is a heuristic (regex / structural) check, not a semantic proof.
These catch clear, mechanical violations of the skill file's structural
requirements. A PASS does not guarantee pedagogical quality; a FAIL is a
strong signal something in the response (or the skill file's wording)
needs attention.

Every rule carries `skill_ref`: the exact line(s) in
iKoott-Assessment-Tutor-Skill.md it is derived from, so failures can be
traced back to the wording that should be tightened.
"""

import re
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class RuleResult:
    rule_id: str
    description: str
    skill_ref: str
    passed: bool
    detail: str


@dataclass
class Rule:
    rule_id: str
    description: str
    skill_ref: str
    check: Callable[[str], "tuple[bool, str]"]


CODE_BLOCK_RE = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
JAVA_CODE_SIGNAL_RE = re.compile(
    r"\b(class\s+\w+|public\s+\w+|private\s+\w+|void\s+\w+\()", re.IGNORECASE
)
DIAGRAM_HINT_RE = re.compile(
    r"(diagram|\[.*->.*\]|-->|<--|\+---|\|\s*\d+\s*\|| / \\ |\\ / )", re.IGNORECASE
)
METHOD_SIG_RE = re.compile(
    # Anchored to the start of a line (past leading whitespace) so a comment's last word
    # can never be mistaken for a return type sitting in front of a later `if (...) {`.
    r"^[ \t]*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+(\w+)\s*\(([^)]*)\)\s*\{",
    re.MULTILINE,
)
GIT_COMMIT_RE = re.compile(r"git\s+commit\s+-m\s+[\"']([^\"']+)[\"']", re.IGNORECASE)

# Java control-flow keywords that look like `name(...) {` but are not method signatures.
CONTROL_FLOW_KEYWORDS = {
    "if", "else", "for", "while", "switch", "catch", "synchronized", "try", "do",
}

# Domain-specific object nouns pulled from the sample assessment (tests/assessment.txt):
# Patient (BST/Queue), Treatment (Stack), Visit/Doctor/Diagnosis (Linked List). Pass 1 must
# stay generic (none of these), Pass 2 must apply to at least one of these real objects.
# Keep this in sync if a different assessment.txt is swapped in.
DOMAIN_WORDS = ["Patient", "Treatment", "Visit", "Doctor", "Diagnosis"]
DOMAIN_OBJECT_RE = re.compile(r"\b(" + "|".join(DOMAIN_WORDS) + r")\w*\b")

# Heading-level signals for where Pass 1 / Pass 2 begin. A response is not required to use
# the literal words "Pass 1"/"Pass 2" verbatim -- the skill file's own section titles are
# "PASS 1 -- Generic" and "PASS 2 -- Apply to Assessment", so a heading built from those same
# words ("Generic Code...", "Assessment Code...", "Bridge...") is an equally valid signal.
PASS1_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}.*\b(pass\s*1|generic)\b.*$", re.IGNORECASE | re.MULTILINE)
PASS2_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}.*\b(pass\s*2|assessment|bridge)\b.*$", re.IGNORECASE | re.MULTILINE)


def _code_blocks(text: str):
    return [(m.group(1), m.group(2), m.start()) for m in CODE_BLOCK_RE.finditer(text)]


def _pass_boundary(text: str, pattern: "re.Pattern") -> int:
    """Return the start index of the earliest heading matching `pattern`, or -1."""
    m = pattern.search(text)
    return m.start() if m else -1


def _pass1_idx(text: str) -> int:
    return _pass_boundary(text, PASS1_HEADING_RE)


def _pass2_idx(text: str) -> int:
    return _pass_boundary(text, PASS2_HEADING_RE)


def check_diagram_before_code(text: str) -> "tuple[bool, str]":
    blocks = _code_blocks(text)
    code_blocks = [b for b in blocks if JAVA_CODE_SIGNAL_RE.search(b[1])]
    if not code_blocks:
        return False, "No code block containing a class/method definition was found at all."
    first_code_pos = code_blocks[0][2]
    pre_code_text = text[:first_code_pos]
    if DIAGRAM_HINT_RE.search(pre_code_text):
        return True, "Found diagram-like content before the first real code block."
    # Fallback: not every diagram uses arrows/box-drawing (e.g. a plain tree sketch with
    # irregular spacing). Any fenced, non-Java block before the first code block is almost
    # certainly the required diagram.
    pre_code_blocks = [b for b in blocks if b[2] < first_code_pos and not JAVA_CODE_SIGNAL_RE.search(b[1])]
    if pre_code_blocks:
        return True, "Found a non-code fenced block before the first real code block (likely a diagram)."
    return False, "No diagram/ASCII-art content detected before the first code block."


def check_file_name_declared(text: str) -> "tuple[bool, str]":
    blocks = _code_blocks(text)
    code_blocks = [b for b in blocks if JAVA_CODE_SIGNAL_RE.search(b[1])]
    if not code_blocks:
        return False, "No code blocks found to check."
    missing = 0
    for _, body, pos in code_blocks:
        preceding = text[max(0, pos - 200):pos]
        inside_start = body[:120]
        has_label = re.search(r"file\s*:\s*\S+\.\w+", preceding, re.IGNORECASE) or re.search(
            r"//\s*file\s*:\s*\S+\.\w+", inside_start, re.IGNORECASE
        )
        if not has_label:
            missing += 1
    if missing == 0:
        return True, f"All {len(code_blocks)} code block(s) preceded by a 'File: X.java' label."
    return False, f"{missing}/{len(code_blocks)} code block(s) missing a preceding 'File: X.java' label."


def _find_method_signatures(body: str):
    """Yield (params_str, method_body_text) for each `name(...) { ... }` found, tolerating
    multi-line parameter lists. The method body is captured by brace-balance matching (not a
    fixed-size window), so it's exact regardless of how many parameters/lines it has, and
    never bleeds into whatever code follows. Skips Java control-flow constructs (if/while/
    for/...) that also look like `word(...) {`."""
    for m in re.finditer(r"\b(\w+)\s*\(", body):
        if m.group(1).lower() in CONTROL_FLOW_KEYWORDS:
            continue
        start_paren = m.end() - 1
        depth = 0
        i = start_paren
        while i < len(body):
            if body[i] == "(":
                depth += 1
            elif body[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        else:
            continue
        end_paren = i
        params_str = body[start_paren + 1:end_paren]
        after_paren = body[end_paren + 1:end_paren + 50]
        brace_match = re.match(r"\s*(throws\s+[\w.,\s]+)?\s*\{", after_paren)
        if not brace_match:
            continue
        if not params_str.strip():
            continue
        brace_pos = end_paren + 1 + after_paren.index("{", brace_match.start())
        depth2 = 0
        j = brace_pos
        while j < len(body):
            if body[j] == "{":
                depth2 += 1
            elif body[j] == "}":
                depth2 -= 1
                if depth2 == 0:
                    break
            j += 1
        else:
            j = len(body) - 1
        method_body = body[brace_pos + 1:j]
        yield params_str, method_body


def _camel_words(name: str) -> "list[str]":
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", name) if len(w) > 1]


def _name_referenced(name: str, comment_text: str) -> bool:
    comment_lower = comment_text.lower()
    if re.search(r"\b" + re.escape(name.lower()) + r"\b", comment_lower):
        return True
    return any(re.search(r"\b" + re.escape(w) + r"\b", comment_lower) for w in _camel_words(name))


def check_inline_arg_comments(text: str) -> "tuple[bool, str]":
    blocks = _code_blocks(text)
    total_methods = 0
    fully_commented = 0
    missing_examples = []
    for _, body, _ in blocks:
        for params_str, method_body in _find_method_signatures(body):
            parts = [p.strip() for p in params_str.split(",") if p.strip()]
            if not parts:
                continue
            # Java's standard `main(String[] args)` boilerplate is exempt: the skill file's
            # own examples never comment it, and it isn't a "concept" being taught.
            if len(parts) == 1 and re.fullmatch(r"String\s*\[\s*\]\s*args", parts[0]):
                continue
            names = []
            for p in parts:
                code_part = p.split("//")[0].strip()
                tokens = re.findall(r"[A-Za-z_]\w*", code_part)
                if tokens:
                    names.append(tokens[-1])
            if not names:
                continue
            total_methods += 1

            # Style A: each parameter sits on its own line with its own trailing comment.
            multiline_ok = len(parts) == len(names) and all("//" in p for p in parts)

            # Style B: a comment block documents each parameter somewhere in the method body
            # -- either right after the opening brace, or (for constructors) on each field's
            # own assignment line (e.g. "this.patientId = patientId; // store the ID"). Matching
            # is camelCase-aware since a natural comment says "store the ID", not "patientId".
            comment_lines = "\n".join(l for l in method_body.splitlines() if "//" in l)
            same_line_ok = bool(comment_lines) and all(_name_referenced(name, comment_lines) for name in names)

            if multiline_ok or same_line_ok:
                fully_commented += 1
            else:
                missing_examples.append(f"({params_str.strip()[:60]})")
    if total_methods == 0:
        return False, "No parameterized method signatures found to check."
    if fully_commented == total_methods:
        return True, f"All {total_methods} parameterized method signature(s) have per-argument inline comments."
    return False, (
        f"{total_methods - fully_commented}/{total_methods} method signature(s) missing "
        f"per-argument inline comments, e.g. {missing_examples[:3]}"
    )


def check_pass1_before_pass2(text: str) -> "tuple[bool, str]":
    pass1_idx = _pass1_idx(text)
    pass2_idx = _pass2_idx(text)
    if pass1_idx == -1 or pass2_idx == -1:
        return False, "Could not locate both a 'Pass 1' and a 'Pass 2' section marker."
    if pass1_idx < pass2_idx:
        return True, "Pass 1 section appears before Pass 2 section."
    return False, "Pass 2 marker appears before (or at the same position as) Pass 1 marker."


def check_pass1_no_assessment_objects(text: str) -> "tuple[bool, str]":
    pass1_idx = _pass1_idx(text)
    pass2_idx = _pass2_idx(text)
    if pass1_idx == -1:
        return False, "No Pass 1 section found."
    end = pass2_idx if pass2_idx != -1 else len(text)
    pass1_text = text[pass1_idx:end]
    pass1_code = "".join(body for _, body, pos in _code_blocks(pass1_text))
    hits = DOMAIN_OBJECT_RE.findall(pass1_code)
    if hits:
        return False, f"Pass 1 code references assessment objects ({set(hits)}) instead of staying generic."
    return True, "Pass 1 code contains no assessment-domain objects."


def check_pass2_uses_assessment_objects(text: str) -> "tuple[bool, str]":
    pass2_idx = _pass2_idx(text)
    if pass2_idx == -1:
        return False, "No Pass 2 section found."
    pass2_text = text[pass2_idx:]
    pass2_code = "".join(body for _, body, pos in _code_blocks(pass2_text))
    if DOMAIN_OBJECT_RE.search(pass2_code):
        return True, "Pass 2 code references a real assessment-domain object."
    return False, "Pass 2 code never references any real assessment-domain object."


def check_one_method_at_a_time(text: str) -> "tuple[bool, str]":
    blocks = _code_blocks(text)
    offenders = []
    for lang, body, _ in blocks:
        sigs = METHOD_SIG_RE.findall(body)
        # A public wrapper calling a private recursive helper of the SAME name (e.g.
        # `public void insert(int value)` -> `private Node insert(Node current, int value)`)
        # is one coherent operation, not two methods -- dedupe by name before counting.
        distinct_names = {s[2] for s in sigs}
        # Constructors count as a "method" for this purpose too.
        if len(distinct_names) > 1:
            offenders.append(len(distinct_names))
    if not offenders:
        return True, "No single code block bundles more than one method."
    return False, f"{len(offenders)} code block(s) contain multiple methods at once (counts: {offenders})."


def check_memorable_rule_present(text: str) -> "tuple[bool, str]":
    if re.search(r"^\s*>\s*.+", text, re.MULTILINE):
        return True, "Found a blockquote line usable as a memorable rule."
    if re.search(r"\*\*[^*\n]{8,100}\*\*", text):
        return True, "Found a short bolded line usable as a memorable rule."
    if re.search(r"(?im)^\s*\*{0,2}rule\*{0,2}\s*:\s*.+", text):
        return True, "Found a line explicitly labeled 'Rule:' usable as a memorable rule."
    return False, "No blockquote, short bolded line, or 'Rule:'-labeled line detected."


def check_generic_main_demo_present(text: str) -> "tuple[bool, str]":
    pass1_idx = _pass1_idx(text)
    pass2_idx = _pass2_idx(text)
    if pass1_idx == -1:
        return False, "No Pass 1 section found."
    end = pass2_idx if pass2_idx != -1 else len(text)
    segment = text[pass1_idx:end]
    if re.search(r"file\s*:\s*main\.java", segment, re.IGNORECASE) or re.search(
        r"class\s+Main\b", segment
    ):
        return True, "Found a generic Main.java demonstration inside Pass 1."
    return False, "No Main.java / class Main demonstration found inside Pass 1."


# The skill file's own instruction for the bridge line (line 78) is to state what CHANGES
# and what stays IDENTICAL. Rather than matching an ever-growing list of exact phrasings
# (every fresh response paraphrases this differently), check for that underlying pair of
# concepts co-occurring near the Pass 2 boundary: a continuity signal and a change signal.
BRIDGE_CONTINUITY_WORDS = ["same", "identical", "unchanged", "remains", "stays", "still the"]
BRIDGE_CHANGE_WORDS = ["changes", "instead of", "different", "now storing", "now using", "swap", "apply"]


def check_bridge_line_present(text: str) -> "tuple[bool, str]":
    pass2_idx = _pass2_idx(text)
    if pass2_idx == -1:
        return False, "No Pass 2 section found."
    # The bridge sentence is sometimes written as prose right before the Pass 2 heading
    # rather than under its own "Bridge" heading, so look a bit before the boundary too,
    # and far enough after it to cover a full paragraph-length bridge.
    window = text[max(0, pass2_idx - 500): pass2_idx + 900].lower()
    has_continuity = any(w in window for w in BRIDGE_CONTINUITY_WORDS)
    has_change = any(w in window for w in BRIDGE_CHANGE_WORDS)
    if has_continuity and has_change:
        return True, "Found bridge-line language (both a continuity and a change signal) near the Pass 2 boundary."
    return False, (
        "No bridge line found near the Pass 2 boundary "
        f"(continuity signal: {has_continuity}, change signal: {has_change})."
    )


def check_assessment_main_demo_present(text: str) -> "tuple[bool, str]":
    pass2_idx = _pass2_idx(text)
    if pass2_idx == -1:
        return False, "No Pass 2 section found."
    segment = text[pass2_idx:]
    has_main = re.search(r"file\s*:\s*main\.java", segment, re.IGNORECASE) or re.search(
        r"class\s+Main\b", segment
    )
    has_domain_object = DOMAIN_OBJECT_RE.search(segment)
    if has_main and has_domain_object:
        return True, "Found a Main demonstration in Pass 2 using a real assessment-domain object."
    return False, "No Main demonstration referencing a real assessment-domain object found in Pass 2."


CHECK_IN_PHRASE_RE = re.compile(
    r"(whenever you'?re ready|when you'?re ready|ready when you are|whenever you are|"
    r"let me know|just say|your call|up to you|take your time)",
    re.IGNORECASE,
)


def check_closing_asks_permission(text: str) -> "tuple[bool, str]":
    tail = text.strip()[-400:]
    if "?" in tail:
        return True, "Response ends with a question (checking in before advancing)."
    if CHECK_IN_PHRASE_RE.search(tail):
        return True, "Response ends with a non-question check-in invitation (e.g. 'whenever you're ready')."
    return False, "Response does not end with a question or check-in phrase — may be auto-advancing instead."


def check_commit_after_full_topic_only(text: str) -> "tuple[bool, str]":
    pass1_idx = _pass1_idx(text)
    pass2_idx = _pass2_idx(text)
    commits = list(GIT_COMMIT_RE.finditer(text))
    if not commits:
        return False, "No 'git commit -m' example found in the response."
    if pass1_idx == -1 or pass2_idx == -1:
        return False, "Cannot verify commit placement without both Pass 1 and Pass 2 markers."
    early_commits = [c for c in commits if pass1_idx < c.start() < pass2_idx]
    if early_commits:
        return False, f"{len(early_commits)} commit(s) shown between Pass 1 and Pass 2 (mid-topic), not after the full topic."
    return True, f"All {len(commits)} commit(s) appear after Pass 2 has started (full topic complete)."


BANNED_COMMIT_PHRASES = ["final commit", "everything", "complete project", "all done", "finished project"]


def check_commit_message_quality(text: str) -> "tuple[bool, str]":
    commits = list(GIT_COMMIT_RE.finditer(text))
    if not commits:
        return False, "No 'git commit -m' example found in the response."
    bad = [c.group(1) for c in commits if any(p in c.group(1).lower() for p in BANNED_COMMIT_PHRASES)]
    if bad:
        return False, f"Commit message(s) look like a giant/final dump, not a scoped topic commit: {bad}"
    return True, f"Commit message(s) look scoped and specific: {[c.group(1) for c in commits]}"


def check_code_blocks_language_tagged(text: str) -> "tuple[bool, str]":
    # Only actual Java source blocks need a language tag to be "copy-paste ready" (skill
    # line 135) -- diagrams and `git`/shell snippets are fenced for readability, not as
    # source the student pastes into their IDE, so they're exempt.
    blocks = [b for b in _code_blocks(text) if JAVA_CODE_SIGNAL_RE.search(b[1])]
    if not blocks:
        return False, "No Java code blocks found to check."
    untagged = [b for b in blocks if not b[0]]
    if untagged:
        return False, f"{len(untagged)}/{len(blocks)} Java code block(s) have no language tag on the fence."
    return True, f"All {len(blocks)} Java code block(s) are language-tagged (copy-paste ready)."


RULES: "list[Rule]" = [
    Rule("diagram_before_code", "A small diagram must appear before any code is shown.",
         "iKoott-Assessment-Tutor-Skill.md:67", check_diagram_before_code),
    Rule("file_name_declared", "Every code block states its file name (e.g. 'File: Node.java').",
         "iKoott-Assessment-Tutor-Skill.md:71", check_file_name_declared),
    Rule("inline_arg_comments", "Every method parameter has its own inline comment.",
         "iKoott-Assessment-Tutor-Skill.md:72", check_inline_arg_comments),
    Rule("pass1_before_pass2", "Pass 1 (generic) must be taught before Pass 2 (assessment).",
         "iKoott-Assessment-Tutor-Skill.md:62-83", check_pass1_before_pass2),
    Rule("pass1_no_assessment_objects", "Pass 1 code must use plain/generic data, not real assessment objects.",
         "iKoott-Assessment-Tutor-Skill.md:62,69", check_pass1_no_assessment_objects),
    Rule("pass2_uses_assessment_objects", "Pass 2 code must use a real assessment-domain object.",
         "iKoott-Assessment-Tutor-Skill.md:76-80", check_pass2_uses_assessment_objects),
    Rule("one_method_at_a_time", "Never combine multiple methods into a single code block.",
         "iKoott-Assessment-Tutor-Skill.md:69", check_one_method_at_a_time),
    Rule("memorable_rule_present", "A short, quotable 'memorable rule' line must be present.",
         "iKoott-Assessment-Tutor-Skill.md:68", check_memorable_rule_present),
    Rule("generic_main_demo_present", "Pass 1 must end with a generic Main.java demonstration.",
         "iKoott-Assessment-Tutor-Skill.md:74", check_generic_main_demo_present),
    Rule("bridge_line_present", "Pass 2 must open with an explicit bridge line.",
         "iKoott-Assessment-Tutor-Skill.md:78", check_bridge_line_present),
    Rule("assessment_main_demo_present", "Pass 2 must end with a real-object Main demonstration.",
         "iKoott-Assessment-Tutor-Skill.md:80", check_assessment_main_demo_present),
    Rule("closing_asks_permission", "Topic closing must check in with the student, never auto-advance.",
         "iKoott-Assessment-Tutor-Skill.md:81,134", check_closing_asks_permission),
    Rule("commit_after_full_topic_only", "Git commit must only be taught after BOTH passes are complete.",
         "iKoott-Assessment-Tutor-Skill.md:95", check_commit_after_full_topic_only),
    Rule("commit_message_quality", "Commit messages must be scoped/specific, never a giant final dump.",
         "iKoott-Assessment-Tutor-Skill.md:105-109", check_commit_message_quality),
    Rule("code_blocks_language_tagged", "Code must be copy-paste-ready (fenced with a language tag).",
         "iKoott-Assessment-Tutor-Skill.md:135", check_code_blocks_language_tagged),
]


def run_all_rules(text: str) -> "list[RuleResult]":
    results = []
    for rule in RULES:
        passed, detail = rule.check(text)
        results.append(RuleResult(rule.rule_id, rule.description, rule.skill_ref, passed, detail))
    return results
