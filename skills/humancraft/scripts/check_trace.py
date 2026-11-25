#!/usr/bin/env python3
"""Offline single-effect workflow invariant checker; does not collect evidence."""

import argparse
import json
import sys
from pathlib import Path

from strict_json import loads

KINDS = {"start", "authorize", "cancel", "commit", "success", "fail"}


def check(data):
    if (
        not isinstance(data, dict)
        or not isinstance(data.get("events"), list)
        or not data["events"]
    ):
        raise ValueError("nonempty events list required")
    states = {}
    writes = set()
    violations = []
    last = 0

    def err(seq, code):
        violations.append({"seq": seq, "code": code})

    for e in data["events"]:
        if not isinstance(e, dict):
            raise ValueError("event object required")
        seq = e.get("seq")
        op = e.get("op")
        kind = e.get("kind")
        scope = e.get("scope")
        if (
            type(seq) is not int
            or seq <= last
            or not all(
                isinstance(x, str) and x.strip() and x == x.strip()
                for x in (op, scope, kind)
            )
            or kind not in KINDS
        ):
            raise ValueError("invalid event or non-increasing sequence")
        last = seq
        if kind == "authorize" and type(e.get("allowed")) is not bool:
            raise ValueError("authorization boolean required")
        if kind == "commit" and (
            not isinstance(e.get("write_id"), str)
            or not e["write_id"].strip()
            or e["write_id"] != e["write_id"].strip()
        ):
            raise ValueError("write_id required")
        if kind == "start":
            if op in states:
                err(seq, "duplicate-start")
            else:
                states[op] = {
                    "scope": scope,
                    "allowed": False,
                    "committed": False,
                    "terminal": False,
                }
            continue
        if op not in states:
            err(seq, "missing-start")
            continue
        st = states[op]
        if scope != st["scope"]:
            err(seq, "scope-changed")
            continue
        if st["terminal"]:
            err(seq, "after-terminal")
            continue
        if kind == "authorize":
            st["allowed"] = e["allowed"]
        elif kind == "commit":
            if not st["allowed"]:
                err(seq, "unauthorized-commit")
            if st["committed"] or e["write_id"] in writes:
                err(seq, "duplicate-effect")
            st["committed"] = True
            writes.add(e["write_id"])
        elif kind in ("success", "fail", "cancel"):
            if kind == "success" and not st["committed"]:
                err(seq, "success-without-commit")
            if kind in ("fail", "cancel") and st["committed"]:
                err(seq, "committed-effect-needs-reconciliation")
            st["terminal"] = True
    for op, st in states.items():
        if not st["terminal"]:
            violations.append({"op": op, "code": "incomplete-operation"})
    return {
        "status": "FAIL" if violations else "PASS",
        "scope": "supplied event invariants only",
        "events": len(data["events"]),
        "operations": len(states),
        "violations": violations,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("trace")
    a = p.parse_args()
    try:
        result = check(loads(Path(a.trace).read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as e:
        print(json.dumps({"status": "INVALID", "error": str(e)}))
        return 2
    print(json.dumps(result, indent=2))
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    sys.exit(main())
