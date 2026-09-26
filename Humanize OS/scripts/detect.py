#!/usr/bin/env python3
"""
detect.py - scan prose for AI writing tells.

Reports line numbers and pattern names so the humanize pass can edit targeted
passages instead of regenerating whole documents.

This is a detection aid. Flags are candidates, not verdicts - see
references/tells.md for when each pattern is legitimate.

Usage:
    python detect.py FILE [--report] [--json] [--min-severity low|medium|high]
    cat draft.md | python detect.py - --report

Only needs the standard library.
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------- patterns

# (name, regex, severity, note)
PHRASE_PATTERNS = [
    ("throat-clearing opener",
     r"(?i)(?:^|(?<=[.!?]\s))\s*(here'?s the thing|it turns out that|the (?:uncomfortable |simple |hard )?truth is|what'?s (?:interesting|fascinating) is|let'?s be (?:honest|clear|real)|make no mistake|at the end of the day|when it comes to|in today'?s [a-z-]+ (?:landscape|world|market|environment)|it'?s worth noting that|it should be noted|it is important to (?:note|remember|understand))",
     "high", "Delete the opener; start at the content."),

    ("meta-commentary",
     r"(?i)\b(?:in this (?:section|article|post|guide)(?:,| we)|before we (?:dive in|begin|get started)|let'?s (?:unpack|dive into|explore|take a look at) (?:this|that)|now that we'?ve covered|as we'?ll see|as mentioned (?:earlier|above))\b",
     "medium", "Headings already do this work."),

    ("reader-trust violation",
     r"(?i)\b(?:let that sink in|think about (?:it|that)|notice how|ask yourself|remember:|and that'?s (?:okay|ok)|don'?t worry|you'?re not alone|here'?s what i mean|what if i told you)\b",
     "high", "State the point; drop the instruction to the reader."),

    ("empty intensifier",
     r"(?i)\b(?:truly|really|very|incredibly|remarkably|absolutely|fundamentally|essentially|in essence|literally|quite simply|simply put)\b",
     "low", "Usually deletable with no loss."),

    ("AI vocabulary",
     r"(?i)\b(?:delve|delves|delving|leverage[sd]?|leveraging|utilize[sd]?|facilitate[sd]?|robust|seamless(?:ly)?|comprehensive|holistic|multifaceted|synerg(?:y|istic)|paradigm shift|game[- ]?chang(?:er|ing)|unlock(?:s|ing)? the|harness(?:es|ing)?|foster(?:s|ing)?|underscore[sd]?|embark(?:s|ing)?|navigat(?:e|es|ing) the|the [a-z]+ landscape|ecosystem|myriad|plethora|testament to)\b",
     "medium", "Replace with the specific thing, not a synonym."),

    ("vague quantifier",
     r"(?i)\b(?:significant(?:ly)?|substantial(?:ly)?|considerable|numerous|various|a (?:wide )?(?:range|variety) of|countless|several key|many of the)\b",
     "medium", "Replace with the number or the consequence, if the source has one."),

    ("vague noun",
     r"(?i)\b(?:stakeholders|the situation|these things|such factors|various aspects|key considerations|best practices|the space)\b",
     "medium", "Name the actual people, event, or objects."),

    ("corporate filler",
     r"(?i)\b(?:lean into|circle back|touch base|move the needle|low[- ]hanging fruit|deep dive|at scale|best[- ]in[- ]class|cutting[- ]edge|state[- ]of[- ]the[- ]art|next[- ]level|world[- ]class)\b",
     "medium", "Cut or say the plain version."),

    ("hedge stack",
     r"(?i)\b(?:it'?s (?:important|worth) (?:to )?(?:noting|remembering|considering)|one might (?:argue|say|consider)|it could be argued|arguably|to some extent|in many ways)\b",
     "low", "Check whether the hedge is load-bearing or reflexive."),
]

STRUCTURE_PATTERNS = [
    ("binary contrast",
     r"(?i)(?:^|(?<=[.!?]\s))\s*(?:not because [^.!?]{3,60}[.!?]\s*because\b|it'?s not (?:about |just )?[^.!?]{3,60}[,.]?\s*it'?s\b|isn'?t (?:about |just )?[^.!?]{3,60}[,.]?\s*it'?s\b)",
     "high", "Fine once; a tic twice; a template three times."),

    ("negative listing",
     r"(?i)(?:^|(?<=[.!?]\s))\s*this (?:isn'?t|is not) (?:a |an |about )[^.!?]{3,60}[.!?]\s*(?:it|and it|nor is it)[^.!?]{0,20}(?:isn'?t|is not)",
     "high", "Defining by elimination before stating the thing."),

    ("rhetorical question setup",
     r"(?i)(?:^|(?<=[.!?]\s))\s*(?:what if|why does|how do|ever wonder|have you ever)[^.!?\n]{5,90}\?",
     "medium", "Check whether the answer follows immediately - if so, just state it."),

    ("dramatic fragment stack",
     r"(?:^|(?<=[.!?]\s))\s*(?:[A-Z][a-z]+\.\s+){3,}",
     "high", "One fragment is emphasis; a stack is a performance."),

    ("slogan closer",
     r"(?i)(?:^|(?<=[.!?]\s))\s*(?:that'?s it\.|that'?s the (?:whole )?\w+\.|full stop\.|period\.|end of story\.|simple as that\.)",
     "high", "Manufactured emphasis."),

    ("em-dash reversal",
     r"(?i)—\s*(?:and that'?s|but that'?s|which is)\b",
     "low", "Check function; em dashes are not automatically a tell."),
]

# Abstract subjects doing human things.
FALSE_AGENCY = re.compile(
    r"(?i)\b(?:the )?(?:data|market|decision|culture|conversation|architecture|"
    r"algorithm|process|system|industry|technology|research|evidence|complaint|"
    r"feedback|strategy|approach|framework|narrative|discourse|landscape)\s+"
    r"(?:tells?|shows?|demands?|wants?|decides?|chooses?|believes?|thinks?|"
    r"knows?|rewards?|punishes?|emerges?|shifts?|moves?|speaks?|suggests?|"
    r"argues?|insists?|refuses?|agrees?)\b"
)

PASSIVE = re.compile(
    r"(?i)\b(?:was|were|is|are|been|being|be)\s+"
    r"(?:\w+ly\s+)?"
    r"(?:made|created|built|decided|reached|believed|considered|thought|"
    r"designed|developed|implemented|established|determined|chosen|selected|"
    r"raised|identified|observed|noted|found|conducted|performed|achieved|"
    r"required|expected|seen|given|taken|used|done)\b"
)

NARRATOR_DISTANCE = re.compile(
    r"(?i)\b(?:people tend to|one (?:might|must|should|can)|nobody (?:designed|"
    r"decided|chose|planned)|this (?:is why|happens because)|it is (?:often |"
    r"generally |widely )?(?:believed|understood|assumed|accepted) that|"
    r"there (?:is|are) a (?:tendency|sense) (?:to|that))\b"
)

# ------------------------------------------------------------ text handling

FENCE = re.compile(r"^\s*(?:```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")


def split_prose(text):
    """Return [(line_no, line)] for prose lines only.

    Code fences, indented code, tables, and front matter are excluded so the
    scanner never flags anything in untouchable content.
    """
    out = []
    in_fence = False
    in_frontmatter = False
    lines = text.split("\n")

    for i, raw in enumerate(lines, start=1):
        if i == 1 and raw.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if raw.strip() == "---":
                in_frontmatter = False
            continue
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if raw.startswith("    ") or raw.startswith("\t"):
            continue
        if raw.lstrip().startswith("|"):
            continue

        cleaned = INLINE_CODE.sub(" ", raw)
        cleaned = URL.sub(" ", cleaned)
        if cleaned.strip():
            out.append((i, cleaned))
    return out


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def sentences_from(prose_lines):
    joined = " ".join(l for _, l in prose_lines)
    joined = re.sub(r"^#+\s*", "", joined)
    parts = [s.strip() for s in SENT_SPLIT.split(joined) if s.strip()]
    return [p for p in parts if len(p.split()) > 1]


# ---------------------------------------------------------------- scanning

def scan(text):
    prose = split_prose(text)
    findings = []

    def add(line_no, category, name, snippet, severity, note):
        findings.append({
            "line": line_no,
            "category": category,
            "pattern": name,
            "match": snippet.strip()[:90],
            "severity": severity,
            "note": note,
        })

    for line_no, line in prose:
        for name, pat, sev, note in PHRASE_PATTERNS:
            for m in re.finditer(pat, line):
                add(line_no, "phrase", name, m.group(0), sev, note)

        for name, pat, sev, note in STRUCTURE_PATTERNS:
            for m in re.finditer(pat, line):
                add(line_no, "structure", name, m.group(0), sev, note)

        for m in FALSE_AGENCY.finditer(line):
            add(line_no, "false-agency", "abstract subject, human verb",
                m.group(0), "high",
                "Who actually did this? Name them ONLY if the source says.")

        for m in PASSIVE.finditer(line):
            add(line_no, "passive", "passive construction", m.group(0), "low",
                "Keep if the actor is unknown, irrelevant, or conventional.")

        for m in NARRATOR_DISTANCE.finditer(line):
            add(line_no, "narrator-distance", "detached narration",
                m.group(0), "medium",
                "Put a real participant in the sentence where the genre allows.")

    return findings, prose


def rhythm(prose_lines):
    sents = sentences_from(prose_lines)
    lengths = [len(s.split()) for s in sents]
    out = {"sentence_count": len(sents), "flags": []}

    if len(lengths) < 3:
        out["mean_length"] = round(statistics.mean(lengths), 1) if lengths else 0
        out["stdev_length"] = 0.0
        return out

    mean = statistics.mean(lengths)
    sd = statistics.pstdev(lengths)
    out["mean_length"] = round(mean, 1)
    out["stdev_length"] = round(sd, 1)

    if sd < 4.5:
        out["flags"].append(
            f"Uniform sentence length (stdev {sd:.1f} words, mean {mean:.1f}). "
            "Natural prose usually swings wider."
        )

    # runs of similar-length sentences
    run = 1
    worst = 1
    worst_at = 0
    for i in range(1, len(lengths)):
        if abs(lengths[i] - lengths[i - 1]) <= 3:
            run += 1
            if run > worst:
                worst, worst_at = run, i - run + 2
        else:
            run = 1
    if worst >= 4:
        out["flags"].append(
            f"{worst} consecutive sentences of near-identical length "
            f"(starting around sentence {worst_at})."
        )

    # repeated sentence openings
    openers = [s.split()[0].lower().strip(",") for s in sents if s.split()]
    rep = 1
    for i in range(1, len(openers)):
        if openers[i] == openers[i - 1]:
            rep += 1
            if rep >= 3:
                out["flags"].append(
                    f"Three or more consecutive sentences opening with "
                    f"'{openers[i]}'."
                )
                break
        else:
            rep = 1

    # triad reflex
    triads = len(re.findall(
        r"\b\w+,\s+\w+,?\s+and\s+\w+\b",
        " ".join(l for _, l in prose_lines)
    ))
    if triads >= 4:
        out["flags"].append(
            f"{triads} three-item lists. Real writing has twos and fives too."
        )

    return out


def paragraphs(text):
    paras = [p for p in re.split(r"\n\s*\n", text)
             if p.strip() and not p.lstrip().startswith(("#", "|", "```", "-", "*"))]
    counts = [len(SENT_SPLIT.split(p.strip())) for p in paras]
    res = {"paragraph_count": len(paras), "flags": []}
    if len(counts) >= 4:
        sd = statistics.pstdev(counts)
        res["stdev_sentences"] = round(sd, 2)
        if sd < 0.8:
            res["flags"].append(
                f"Paragraphs are uniformly {statistics.mean(counts):.1f} "
                "sentences long. Vary the shape."
            )
    return res


SEV_ORDER = {"low": 0, "medium": 1, "high": 2}


def report(findings, rhy, para, path):
    lines = []
    lines.append(f"AI-tell scan: {path}")
    lines.append("=" * 60)

    if not findings:
        lines.append("\nNo phrase or structure patterns flagged.")
    else:
        by_cat = {}
        for f in findings:
            by_cat.setdefault(f["category"], []).append(f)

        counts = ", ".join(f"{k} {len(v)}" for k, v in sorted(by_cat.items()))
        lines.append(f"\n{len(findings)} flags ({counts})\n")

        for cat in sorted(by_cat):
            lines.append(f"\n--- {cat.upper()} ---")
            items = sorted(by_cat[cat],
                           key=lambda f: (-SEV_ORDER[f["severity"]], f["line"]))
            seen_note = set()
            for f in items:
                lines.append(
                    f"  L{f['line']:<4} [{f['severity']:<6}] "
                    f"{f['pattern']}: \"{f['match']}\""
                )
                if f["note"] not in seen_note:
                    lines.append(f"         -> {f['note']}")
                    seen_note.add(f["note"])

    lines.append("\n--- RHYTHM ---")
    lines.append(
        f"  {rhy['sentence_count']} sentences, mean {rhy.get('mean_length', 0)} "
        f"words, stdev {rhy.get('stdev_length', 0)}"
    )
    for f in rhy["flags"]:
        lines.append(f"  ! {f}")
    if not rhy["flags"]:
        lines.append("  Sentence variation looks natural.")

    lines.append(f"\n  {para['paragraph_count']} prose paragraphs")
    for f in para["flags"]:
        lines.append(f"  ! {f}")

    lines.append("\n" + "=" * 60)
    lines.append("Flags are candidates, not verdicts. Check references/tells.md")
    lines.append("for when each pattern is legitimate. Do not fix mechanically.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Scan prose for AI writing tells.")
    ap.add_argument("file", help="file to scan, or - for stdin")
    ap.add_argument("--report", action="store_true", help="human-readable output")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--min-severity", choices=["low", "medium", "high"],
                    default="low")
    args = ap.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
        name = "<stdin>"
    else:
        p = Path(args.file)
        if not p.exists():
            sys.exit(f"No such file: {p}")
        text = p.read_text(encoding="utf-8", errors="replace")
        name = str(p)

    findings, prose = scan(text)
    findings = [f for f in findings
                if SEV_ORDER[f["severity"]] >= SEV_ORDER[args.min_severity]]
    rhy = rhythm(prose)
    para = paragraphs(text)

    if args.json:
        print(json.dumps({"file": name, "findings": findings,
                          "rhythm": rhy, "paragraphs": para}, indent=2))
    else:
        print(report(findings, rhy, para, name))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # piping into head/less closes stdout early; exit quietly
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
