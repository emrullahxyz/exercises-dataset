#!/usr/bin/env python3
"""Dataset integrity checks for exercises-dataset.

Usage:
  python .claude/scripts/validate_dataset.py            # full audit (fails on any problem)
  python .claude/scripts/validate_dataset.py --strict   # also report orphan media files
  python .claude/scripts/validate_dataset.py --hook      # PostToolUse mode: reads hook JSON on
                                                          # stdin, only runs when data/exercises.json
                                                          # was the edited file.

Exit codes: 0 = clean, 2 = problems found (surfaces stderr back to Claude when run as a hook).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data", "exercises.json")


def _rel(*p):
    return os.path.join(ROOT, *p)


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def audit(strict=False):
    problems = []
    try:
        records = load()
    except Exception as e:
        return [f"exercises.json does not parse as JSON: {e}"]

    if not isinstance(records, list):
        return ["exercises.json must be a top-level JSON array"]

    seen_ids = {}
    referenced = set()
    for i, ex in enumerate(records):
        where = f"[{i}] id={ex.get('id')!r} name={ex.get('name')!r}"
        # id must be unique
        eid = ex.get("id")
        if eid in seen_ids:
            problems.append(f"duplicate id {eid!r} ({where} and {seen_ids[eid]})")
        else:
            seen_ids[eid] = where
        # required media must exist on disk
        for field in ("image", "gif_url"):
            path = ex.get(field)
            if not path:
                problems.append(f"missing '{field}' {where}")
                continue
            referenced.add(path.replace("\\", "/"))
            if not os.path.exists(_rel(*path.split("/"))):
                problems.append(f"{field} file not found: {path} ({where})")
        # mojibake guard: Cyrillic chars leaking into names (e.g. 'sled 45в°')
        name = ex.get("name") or ""
        if re.search(r"[Ѐ-ӿ]", name):
            problems.append(f"non-Latin (mojibake?) character in name: {name!r} ({where})")

    if strict:
        for sub in ("images", "videos"):
            d = _rel(sub)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                rel = f"{sub}/{fn}"
                if rel not in referenced:
                    problems.append(f"orphan media file (not referenced by any record): {rel}")

    return problems


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        try:
            payload = json.load(sys.stdin)
        except Exception:
            return 0  # not a hook invocation we understand; stay out of the way
        fp = (payload.get("tool_input") or {}).get("file_path", "") or ""
        if not fp.replace("\\", "/").endswith("data/exercises.json"):
            return 0  # unrelated edit — nothing to check
        problems = audit(strict=False)
        if problems:
            sys.stderr.write("data/exercises.json failed integrity check:\n")
            sys.stderr.write("\n".join(f"  - {p}" for p in problems) + "\n")
            return 2
        print(f"exercises.json OK ({len(load())} records)")
        return 0

    strict = "--strict" in args
    problems = audit(strict=strict)
    if problems:
        print(f"FAIL — {len(problems)} problem(s):", file=sys.stderr)
        print("\n".join(f"  - {p}" for p in problems), file=sys.stderr)
        return 2
    print(f"OK — {len(load())} records, all media present"
          + (", no orphan files" if strict else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
