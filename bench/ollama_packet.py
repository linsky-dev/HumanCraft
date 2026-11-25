"""在本机 Ollama 上执行单个合成评测任务包，保存原始响应与运行遥测。"""

import argparse
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:11434"
REFERENCE_NAMES = ("behavior-contracts.md", "interaction.md", "verification.md")


def load_guidance(packet):
    skill_dir = packet / "skills"
    chunks = []
    for entry in sorted(skill_dir.glob("*/SKILL.md")):
        chunks.append(entry.read_text(encoding="utf-8"))
        for name in REFERENCE_NAMES:
            reference = entry.parent / "references" / name
            if reference.is_file():
                chunks.append(reference.read_text(encoding="utf-8"))
    return chunks


def run_packet(packet, output, model, seed):
    task = (packet / "TASK.txt").read_text(encoding="utf-8")
    starter = (packet / "app.html").read_text(encoding="utf-8")
    guidance = load_guidance(packet)
    prompt = "\n\n".join([
        "Return only the complete revised HTML document, optionally in one HTML fence.",
        *guidance,
        task,
        "Initial app.html:\n" + starter,
    ])
    options = {"temperature": 0, "seed": seed, "num_ctx": 16384, "num_predict": 4096}
    payload = {"model": model, "prompt": prompt, "stream": False, "think": False, "options": options}
    output.mkdir(parents=True, exist_ok=False)
    (output / "request.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    started = time.monotonic()
    response = None
    error = None
    stage = "infrastructure"
    try:
        request = Request(BASE_URL + "/api/generate", data=json.dumps(payload).encode("utf-8"),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=180) as connection:
            response = json.load(connection)
        (output / "response.json").write_text(json.dumps(response, indent=2), encoding="utf-8")
        if not isinstance(response, dict) or not isinstance(response.get("response"), str):
            raise ValueError("Unrecognized Ollama response")
        stage = "model_output"
        text = response["response"].strip()
        fenced = re.fullmatch(r"```(?:html)?\s*(.*?)\s*```", text, flags=re.IGNORECASE | re.DOTALL)
        html = fenced.group(1).strip() if fenced else text
        if (not response.get("done") or response.get("done_reason") == "length"
                or not re.match(r"<(?:(?:!doctype\s+html)|html)\b", html, re.IGNORECASE)
                or not html.lower().endswith("</html>")):
            raise ValueError("Model did not return a complete HTML document")
        stage = "infrastructure"
        (packet / "app.html").write_text(html + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError) as issue:
        error = str(issue)
    response = response if isinstance(response, dict) else {}
    telemetry = {
        "seconds": round(time.monotonic() - started, 3),
        "input_tokens": response.get("prompt_eval_count") if response else None,
        "output_tokens": response.get("eval_count") if response else None,
        "explicit_guidance_included": bool(guidance),
        "automatic_activation_observed": None,
        "error": error,
        "error_kind": stage if error else None,
    }
    (output / "telemetry.json").write_text(json.dumps(telemetry, indent=2), encoding="utf-8")
    return error is None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    return 0 if run_packet(args.packet, args.output, args.model, args.seed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
