---
name: skills-humancraft-references-event-evidence
description: 'HumanCraft supporting resource: Event evidence for consequential workflows.
  Read only when relevant to the current task.'
---

# Event evidence for consequential workflows

A UI that says “saved”, “cancelled” or “approved” is not evidence of the underlying state. For high-impact workflows collect an independent, sanitized chronological event trace from controlled tests and authoritative sources. Use actual operation IDs, consistent actor/scope, and a unique logical write ID per committed effect. Never include credentials, raw personal records or production secrets. This lightweight checker detects only the invariants described here; it is not a security scanner, backend monitor, or proof of completeness.

`python scripts/check_trace.py assets/trace-example.json` returns JSON and exit 0 only when the modeled checks pass. Exit 1 means violation; exit 2 means malformed/unverifiable data. Use an isolated test harness, not production. Do not fabricate event traces to satisfy a gate.

Trace schema: object with `events` (nonempty ordered list). Each event has `seq` (positive increasing integer), `op` (nonempty operation ID), `kind` (one of start, authorize, cancel, commit, success, fail), `scope` (nonempty stable target identifier). `authorize` includes `allowed` boolean; `commit` includes `write_id` (nonempty globally unique effect ID). An operation starts once; authorization is explicitly granted for the stable scope before any commit. Cancellation after commit is not modeled as rollback: use a separate compensating operation and test actual outcomes. This protocol models single-effect operations with one commit per op; represent batch rows as separate operations. For a read-only workflow use other tests. Every started operation must terminate via success, fail or cancel. Success requires a prior commit. The checker rejects writes after terminal events, repeated write IDs, changed target, missing authorization, missing receipt and incomplete operations. Fail following commit is a reconciliation-required violation; inspect actual state and provide an accurate receipt. A retry is a new operation with the same logical write ID if the intended effect is the same.

Limitations: the checker trusts the input's order and claimed events; it cannot detect unlogged effects, forged authorization, broken instrumentation, real races, privacy violations, or actual durability. Independently compare logs with persisted effects, and use backend permission and concurrency tests. Record run commands, version and scope. A missing trace means NOT_RUN, never PASS.
