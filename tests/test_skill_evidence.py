"""验证公开技能包的两个命令行入口及关键门禁。"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills" / "humancraft"
DIMENSIONS = (
    "outcome",
    "interaction",
    "complexity",
    "resilience",
    "accessibility",
    "emotion",
    "control",
    "delivery",
)
GATES = ("authorization", "integrity", "recovery", "accessible_core", "control")


class EvidenceTests(unittest.TestCase):
    def run_script(self, script, raw):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "证据 空格.json"
            path.write_text(raw, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SKILL / "scripts" / script), str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )

    def make_audit(self, evidence_type):
        observed = {"evidence_type": evidence_type, "evidence": ["run-1"]}
        return {
            "dimensions": {name: dict(observed, score=4) for name in DIMENSIONS},
            "gates": {name: dict(observed, status="pass") for name in GATES},
        }

    def test_inspection_pass_blocks_but_preserves_a_known_failure(self):
        audit = self.make_audit("observed_inspection")
        audit["gates"]["recovery"]["status"] = "fail"
        result = self.run_script("audit_score.py", json.dumps(audit))
        self.assertEqual(result.returncode, 0, result.stderr)
        score = json.loads(result.stdout)
        self.assertEqual(score["observed_score"], 100)
        self.assertEqual(score["gate_status"], "blocked")
        self.assertIn("recovery:fail", score["critical_blockers"])
        self.assertIn(
            "authorization:executed-test-required", score["critical_blockers"]
        )

    def test_executed_tests_satisfy_gate_evidence_requirement(self):
        result = self.run_script(
            "audit_score.py", json.dumps(self.make_audit("observed_test"))
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["critical_blockers"], [])

    def test_unknown_and_all_na_remain_blocked(self):
        audit = self.make_audit("observed_test")
        audit["gates"]["control"] = {"status": "unknown"}
        result = self.run_script("audit_score.py", json.dumps(audit))
        self.assertIn("control:unknown", json.loads(result.stdout)["critical_blockers"])
        audit["gates"] = {
            name: {"status": "na", "reason": "out of scope"} for name in GATES
        }
        result = self.run_script("audit_score.py", json.dumps(audit))
        self.assertIn(
            "all-gates-na-requires-independent-scope-review",
            json.loads(result.stdout)["critical_blockers"],
        )

    def test_both_clis_reject_ambiguous_or_nonstandard_json(self):
        audit = json.dumps(self.make_audit("observed_test"))
        trace = (SKILL / "assets" / "trace-example.json").read_text(encoding="utf-8")
        samples = {
            "audit_score.py": (
                audit.replace(
                    '"status": "pass"', '"status": "fail", "status": "pass"', 1
                ),
                1,
            ),
            "check_trace.py": (
                trace.replace('"kind":', '"kind": "fail", "kind":', 1),
                2,
            ),
        }
        for script, (duplicate, invalid_exit) in samples.items():
            valid = audit if script == "audit_score.py" else trace
            for malformed in (duplicate, valid.replace("{", '{"extra":NaN,', 1)):
                with self.subTest(script=script, input=malformed[:60]):
                    result = self.run_script(script, malformed)
                    self.assertEqual(result.returncode, invalid_exit)

    def test_legacy_example_and_late_commit(self):
        trace = json.loads(
            (SKILL / "assets" / "trace-example.json").read_text(encoding="utf-8")
        )
        result = self.run_script("check_trace.py", json.dumps(trace))
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")
        trace["events"][1]["kind"] = "cancel"
        result = self.run_script("check_trace.py", json.dumps(trace))
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "after-terminal",
            {v["code"] for v in json.loads(result.stdout)["violations"]},
        )
