#!/usr/bin/env python3
"""Bake RENDEZVOUS_SERVER + RS_PUB_KEY into hbb_common config.rs before compile."""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

host = os.environ.get("RENDEZVOUS_SERVER", "").strip()
key = os.environ.get("RS_PUB_KEY", "").strip()
if not host or not key:
    print("RENDEZVOUS_SERVER and RS_PUB_KEY are required", file=sys.stderr)
    sys.exit(1)

candidates = [
    Path("libs/hbb_common/src/config.rs"),
    Path("src/config.rs"),
]
path = next((p for p in candidates if p.is_file()), None)
if path is None:
    print("config.rs not found", file=sys.stderr)
    sys.exit(1)

text = path.read_text(encoding="utf-8")
orig = text

# Bake public key constant
text, n1 = re.subn(
    r'(pub const RS_PUB_KEY:\s*&str\s*=\s*)"[^"]*"',
    rf'\1"{key}"',
    text,
    count=1,
)
# Bake production rendezvous host (runtime static)
text, n2 = re.subn(
    r'(pub static ref PROD_RENDEZVOUS_SERVER:\s*RwLock<String>\s*=\s*RwLock::new\()""\.to_owned\(\)(\);)',
    rf'\1"{host}".to_owned()\2',
    text,
    count=1,
)
# Fallback: also force default rendezvous server list first entry
text, n3 = re.subn(
    r'(pub const RENDEZVOUS_SERVERS:\s*&\[&str\]\s*=\s*&\[)"[^"]*"',
    rf'\1"{host}"',
    text,
    count=1,
)

if text == orig or (n1 < 1):
    print(f"Patch failed (key={n1} prod={n2} servers={n3})", file=sys.stderr)
    sys.exit(1)

path.write_text(text, encoding="utf-8")
print(f"Patched {path}: key={n1} prod={n2} servers={n3} host={host}")
