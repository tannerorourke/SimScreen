#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project_dir:
        return 0

    session_id = payload.get("session_id") or "no-session"
    trace_dir = Path(project_dir) / "traces" / session_id

    try:
        trace_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return 0

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": payload.get("hook_event_name") or payload.get("event") or "unknown",
        "session_id": session_id,
        "agent_id": payload.get("agent_id"),
        "agent_type": payload.get("agent_type"),
        "tool_name": payload.get("tool_name"),
        "tool_use_id": payload.get("tool_use_id"),
        "tool_input": payload.get("tool_input"),
        "tool_response": payload.get("tool_response"),
    }

    try:
        with (trace_dir / "tools.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")
    except OSError:
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
