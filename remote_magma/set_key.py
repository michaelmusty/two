"""Set COCALC_ACCOUNT_API_KEY in the repo-root .env without echoing it.

Reads the key from a hidden prompt (or stdin if piped), rewrites the existing
assignment in place -- preserving every other line and its order -- appends it
if absent, keeps a .env.bak of the previous contents, and tightens the mode to
0600. Prints only the key's length and prefix, never the key.

    python3 remote_magma/set_key.py
"""
import getpass
import os
import re
import sys
from pathlib import Path

VAR = "COCALC_ACCOUNT_API_KEY"
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def main():
    if sys.stdin.isatty():
        key = getpass.getpass(f"{VAR} (input hidden): ").strip()
    else:
        key = sys.stdin.read().strip()

    if not key:
        print("no key given; .env unchanged", file=sys.stderr)
        return 1
    if any(c.isspace() for c in key):
        print("key contains whitespace; refusing", file=sys.stderr)
        return 1
    if not key.startswith("sk"):
        print(f"warning: key does not start with 'sk' (got {key[:2]!r})", file=sys.stderr)

    text = ENV_PATH.read_text() if ENV_PATH.is_file() else ""
    if text and not text.endswith("\n"):
        text += "\n"
    if text:
        Path(str(ENV_PATH) + ".bak").write_text(text)
        os.chmod(str(ENV_PATH) + ".bak", 0o600)

    line = f"{VAR}={key}"
    text, n = re.subn(rf"(?m)^{VAR}=.*$", lambda _: line, text)
    if n == 0:
        text += line + "\n"
        where = "appended"
    else:
        where = f"replaced ({n} occurrence{'s' if n > 1 else ''})"

    ENV_PATH.write_text(text)
    os.chmod(ENV_PATH, 0o600)
    print(f"{VAR} {where} in {ENV_PATH}: length {len(key)}, prefix {key[:5]}...")
    print("previous contents saved to .env.bak (also 0600, gitignored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
