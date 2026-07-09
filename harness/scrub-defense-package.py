#!/usr/bin/env python3
"""Scrub GitHub account identifiers from the defense package.

The repo remote lives under a GitHub account whose name must not appear in the
defense deliverables; every occurrence is replaced by the <TAI-KHOAN-GITHUB>
placeholder for the student to fill in with their own account. Handles:
markdown/text files, the report DOCX, the slide PPTX, and text files inside
the source snapshot zip. Midscene HTML reports are left untouched on purpose —
their only "cpk" hits are base64 coincidences inside embedded screenshots.

Usage: python3 harness/scrub-defense-package.py <package-dir>
"""

import io
import os
import re
import sys
import zipfile

ACCOUNT = "cpk"
# Square brackets: must stay valid inside OOXML text nodes (no angle brackets).
PLACEHOLDER = "[TAI-KHOAN-GITHUB]"
# Alphanumeric boundaries: matches `/cpk/` in URLs and `cpk-code` in paths but
# never base64 runs like "...vcpkqqh..." (those sit between letters). Base64
# blobs only live in binary parts and the excluded HTML reports anyway.
PATTERN = re.compile(r"(?<![A-Za-z0-9])" + ACCOUNT + r"(?![A-Za-z0-9])")

TEXT_EXT = {".md", ".txt", ".ts", ".tsx", ".js", ".mjs", ".json", ".css",
            ".html", ".yml", ".yaml", ".sh", ".py", ".gitignore", ".example"}


def scrub_text(data):
    return PATTERN.sub(PLACEHOLDER, data)


def scrub_plain_file(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    new = scrub_text(data)
    if new != data:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        return True
    return False


def scrub_docx_pptx(path):
    """Replace inside XML parts of an OOXML container, preserving all else."""
    changed = False
    src = zipfile.ZipFile(path)
    buf = io.BytesIO()
    out = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename.endswith(".xml"):
            text = data.decode("utf-8")
            new = scrub_text(text)
            if new != text:
                data = new.encode("utf-8")
                changed = True
        out.writestr(item, data)
    out.close()
    src.close()
    if changed:
        with open(path, "wb") as f:
            f.write(buf.getvalue())
    return changed


def scrub_zip(path):
    """Rewrite text files inside the source snapshot zip."""
    changed = False
    src = zipfile.ZipFile(path)
    buf = io.BytesIO()
    out = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    for item in src.infolist():
        data = src.read(item.filename)
        ext = os.path.splitext(item.filename)[1].lower()
        base = os.path.basename(item.filename)
        if ext in TEXT_EXT or base in ("CLAUDE.md", ".env.example"):
            try:
                text = data.decode("utf-8")
                new = scrub_text(text)
                if new != text:
                    data = new.encode("utf-8")
                    changed = True
            except UnicodeDecodeError:
                pass
        out.writestr(item, data)
    out.close()
    src.close()
    if changed:
        with open(path, "wb") as f:
            f.write(buf.getvalue())
    return changed


def main():
    root = sys.argv[1]
    touched = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            ext = os.path.splitext(fn)[1].lower()
            if rel.startswith("05-demo-offline") and ext == ".html":
                continue  # base64-only coincidences; do not touch
            if ext in (".md", ".txt", ".csv"):
                if scrub_plain_file(path):
                    touched.append(rel)
            elif ext in (".docx", ".pptx"):
                if scrub_docx_pptx(path):
                    touched.append(rel)
            elif ext == ".zip":
                if scrub_zip(path):
                    touched.append(rel)
    print("scrubbed:", *touched, sep="\n  " if touched else " nothing")


if __name__ == "__main__":
    main()
