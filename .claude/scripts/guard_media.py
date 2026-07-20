#!/usr/bin/env python3
"""PreToolUse guard: block Bash commands that would delete the irreplaceable
images/ or videos/ media directories (2,652 un-regenerable assets).

Reads the hook JSON on stdin. Exit 2 blocks the tool call and shows stderr to Claude.
"""
import json
import re
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    low = cmd.lower()

    # deletion verbs targeting the media dirs (leading boundary avoids matching
    # 'rm' inside words like 'perform'/'reform')
    deletes = r"(^|[\s;&|(])(rm|rmdir|rd|del|ri)\s|remove-item|(^|[\s;&|(])find\b.*-delete|git\s+rm\b"
    targets = r"\b(images|videos)([\\/ ]|['\"]|$)"
    if re.search(deletes, low) and re.search(targets, low):
        sys.stderr.write(
            "BLOCKED: this command targets images/ or videos/, which hold 2,652 "
            "irreplaceable, un-regenerable media files with no build step to recreate them.\n"
            "If this is intentional, run it manually outside Claude.\n"
            f"Command: {cmd}\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
