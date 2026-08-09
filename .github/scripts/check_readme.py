#!/usr/bin/env python3
"""Conservative README checker/fixer.

- Finds HTTP(S) links in README.md and verifies them (HTTP GET with short timeout).
- Performs only safe, obvious replacements (http://github.com -> https://github.com, http -> https for shields.io/badge URLs).
- Writes back README.md only when edits are made so the workflow commit step can pick them up.
- Exits 0 on success (even if broken links found); non-zero only on unexpected errors.
"""

from __future__ import annotations
import re
import sys
import ssl
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import List, Tuple

README = "README.md"
TIMEOUT = 10

LINK_RE = re.compile(r"\[(?:[^\]]+)\]\((https?://[^)\s]+)\)")
URL_RE = re.compile(r"https?://[^)\s]+")


def find_links(text: str) -> List[str]:
    links = LINK_RE.findall(text)
    # also capture bare URLs not in markdown link form
    # but favor bracketed links for minimal edits
    return links


def check_url(url: str) -> Tuple[bool, str]:
    """Return (ok, message). ok=True if reachable."""
    try:
        req = Request(url, method="HEAD")
        # some servers don't like HEAD; fall back to GET if HEAD fails
        try:
            with urlopen(req, timeout=TIMEOUT) as resp:
                code = getattr(resp, 'status', None) or getattr(resp, 'getcode', None)
                if code and 200 <= int(code) < 400:
                    return True, f"{code}"
                return False, f"HTTP {code}"
        except (HTTPError, URLError) as e:
            # try GET as fallback
            try:
                req2 = Request(url, method="GET")
                with urlopen(req2, timeout=TIMEOUT) as resp:
                    code = getattr(resp, 'status', None) or getattr(resp, 'getcode', None)
                    if code and 200 <= int(code) < 400:
                        return True, f"{code}"
                    return False, f"HTTP {code}"
            except Exception as e2:
                return False, str(e2)
    except TypeError:
        # older Python may not accept method on Request; fallback to GET
        try:
            with urlopen(url, timeout=TIMEOUT) as resp:
                code = getattr(resp, 'status', None) or getattr(resp, 'getcode', None)
                if code and 200 <= int(code) < 400:
                    return True, f"{code}"
                return False, f"HTTP {code}"
        except Exception as e:
            return False, str(e)
    except Exception as e:
        return False, str(e)


def safe_replacements(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Perform conservative, obvious replacements and return new text and list of (old,new)."""
    changes: List[Tuple[str, str]] = []

    def replace_once(old: str, new: str):
        nonlocal text
        if old in text:
            text = text.replace(old, new)
            changes.append((old, new))

    # Common: upgrade github links to https
    replace_once("http://github.com", "https://github.com")
    replace_once("http://www.github.com", "https://www.github.com")

    # Shields/badge endpoints should be HTTPS
    replace_once("http://img.shields.io", "https://img.shields.io")
    replace_once("http://shields.io", "https://shields.io")

    # Some raw github content
    replace_once("http://raw.githubusercontent.com", "https://raw.githubusercontent.com")

    return text, changes


def main() -> int:
    try:
        with open(README, 'r', encoding='utf-8') as f:
            txt = f.read()
    except FileNotFoundError:
        print(f"{README} not found; nothing to do.")
        return 0

    original = txt
    txt_after, edits = safe_replacements(txt)

    broken_links = []

    links = find_links(txt_after)
    for url in links:
        ok, msg = check_url(url)
        if not ok:
            broken_links.append((url, msg))

    # Print a concise summary for logs
    if edits:
        print("Applied safe edits:")
        for old, new in edits:
            print(f" - {old} -> {new}")

    if broken_links:
        print("Broken or unreachable links detected (non-fatal):")
        for url, reason in broken_links:
            print(f" - {url}: {reason}")
    else:
        print("No broken links detected among checked URLs.")

    if txt_after != original:
        try:
            with open(README, 'w', encoding='utf-8') as f:
                f.write(txt_after)
            print("Wrote README.md with safe edits.")
        except Exception as e:
            print("Failed to write README.md:", e)
            return 1

    # Always exit 0 on expected behavior; non-zero only on unexpected errors
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print("Unexpected error:", e)
        sys.exit(1)
