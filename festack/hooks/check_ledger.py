#!/usr/bin/env python3
"""festack last-look hook core.

Reads a JSON payload on stdin describing an outward-facing send, checks active
engagement ledgers for the review state of any referenced artifact, prints at most one
awareness line to stdout (never blocks), and appends an outbound receipt to the
matching log.md.

Contract: ALWAYS exits 0 (fail-open). This script must never be able to stop a send.
Accepts either the neutral adapter shape {"text", "channel", "external"} or a raw
Claude Code PreToolUse payload {"tool_name", "tool_input"} which it translates itself.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path


def festack_home():
    env = os.environ.get("FESTACK_HOME")
    if env:
        return Path(env)
    for candidate in (Path.home() / ".claude/festack", Path.home() / ".cursor/festack"):
        if candidate.exists():
            return candidate
    return None


def adapt_host_payload(payload: dict) -> dict:
    """Translate a raw Claude Code PreToolUse payload into the neutral shape.

    Externality is positive-evidence only: gmail sends are external iff
    FESTACK_ORG_DOMAIN is set and a to/cc/bcc address resolves to another domain.
    Raw drive/slack payloads cannot prove externality, so external stays unset
    (the hook then stays silent and writes nothing).
    """
    tool_name = str(payload.get("tool_name", "")).lower()
    tool_input = payload.get("tool_input", {})
    if "gmail" in tool_name:
        channel = "gmail"
    elif "drive" in tool_name:
        channel = "drive"
    elif "slack" in tool_name:
        channel = "slack"
    else:
        channel = tool_name
    adapted = {"text": json.dumps(tool_input), "channel": channel}
    org_domain = os.environ.get("FESTACK_ORG_DOMAIN", "").strip().lower()
    if channel == "gmail" and org_domain and isinstance(tool_input, dict):
        recipients = []
        for key, value in tool_input.items():
            key_parts = re.split(r"[^a-z]+", str(key).lower())
            if not any(part in ("to", "cc", "bcc") for part in key_parts):
                continue
            values = value if isinstance(value, list) else [value]
            recipients.extend(str(v) for v in values)
        for recipient in recipients:
            for domain in re.findall(r"@([\w.-]+)", recipient):
                if domain.lower().strip(".") != org_domain:
                    adapted["external"] = True
    return adapted


def active_slugs(engagements: Path) -> list:
    index = engagements / "ENGAGEMENTS.md"
    if not index.exists():
        return []
    slugs = []
    for line in index.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[2] in ("active", "dormant") and cells[0] != "slug":
            slugs.append(cells[0])
    return slugs


ARTIFACT = re.compile(r"artifact:\s*([^|]+?)\s+v(\d+)")


def artifact_states(log_text: str) -> dict:
    """name -> {latest: int, reviewed: set[int]} from receipt lines.

    Only review receipts count toward reviewed state: outbound receipts are
    audit lines, and their "review state at send: unreviewed" tail must never
    be misread as a review (it contains the substring "reviewed").
    """
    states = {}
    for line in log_text.splitlines():
        match = ARTIFACT.search(line)
        if not match:
            continue
        name, version = match.group(1).strip(), int(match.group(2))
        state = states.setdefault(name, {"latest": 0, "reviewed": set()})
        state["latest"] = max(state["latest"], version)
        fields = [c.strip() for c in line.split("|")]
        is_outbound = len(fields) >= 2 and fields[1] == "outbound"
        tail = fields[-1] if fields else ""
        if not is_outbound and "reviewed" in tail and "unreviewed" not in tail:
            state["reviewed"].add(version)
    return states


def mentions(name: str, text: str) -> bool:
    """Word-boundary artifact match: 'dbs-onepager' must not fire on text that
    only mentions 'dbs-onepager-final' (hyphen counts as a word character)."""
    return re.search(rf"(?<![\w-]){re.escape(name.lower())}(?![\w-])", text.lower()) is not None


def main() -> None:
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        return
    if "tool_name" in payload:
        payload = adapt_host_payload(payload)
    text = str(payload.get("text", ""))
    channel = str(payload.get("channel", "unknown"))
    # Outward-detection rule: adapters set external=True only on positive evidence
    # (recipient outside the org domain, shared/external Slack channel, Drive share
    # outside the org). Can't tell -> stay silent, write no receipt.
    if payload.get("external") is not True:
        return
    home = festack_home()
    if not home or not text:
        return
    engagements = home / "engagements"
    today = datetime.date.today().isoformat()
    for slug in active_slugs(engagements):
        log_path = engagements / slug / "log.md"
        if not log_path.exists():
            continue
        log_text = log_path.read_text(encoding="utf-8")
        needs_newline = bool(log_text) and not log_text.endswith("\n")
        for name, state in artifact_states(log_text).items():
            if not mentions(name, text):
                continue
            latest, reviewed = state["latest"], state["reviewed"]
            review_state = "reviewed" if latest in reviewed else "unreviewed"
            if review_state == "unreviewed":
                if reviewed:
                    print(f"last-look: {name} v{latest} edited since its last review (v{max(reviewed)}) - send is proceeding.")
                else:
                    print(f"last-look: no review on record for {name} - send is proceeding.")
            with log_path.open("a", encoding="utf-8") as log_file:
                if needs_newline:
                    log_file.write("\n")
                    needs_newline = False
                log_file.write(
                    f"{today} | outbound | artifact: {name} v{latest} | sent via {channel} | review state at send: {review_state}\n"
                )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail-open: a broken hook must never affect a send
    sys.exit(0)
