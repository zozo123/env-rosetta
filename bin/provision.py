"""Provision 4 islo sandboxes, one per framework. Writes share URLs to cards/<fw>.json."""
from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"
ISLO = os.environ.get("ISLO_BIN", "islo")

FRAMEWORKS = {
    "openenv": {
        "name": "OpenEnv",
        "vendor": "Meta",
        "sandbox": "rosetta-openenv",
        "port": 8080,
        "start": "uvicorn server.app:app --host 0.0.0.0 --port 8080",
        "env_path": "envs/wordle_env/openenv",
        "color": "#3a86ff",
    },
    "ors": {
        "name": "ORS",
        "vendor": "Open Reward Standard",
        "sandbox": "rosetta-ors",
        "port": 8080,
        "start": "python server.py --port 8080",
        "env_path": "envs/wordle_env/ors",
        "color": "#ff006e",
    },
    "nemo_gym": {
        "name": "NeMo Gym",
        "vendor": "NVIDIA",
        "sandbox": "rosetta-nemo-gym",
        "port": 11000,
        "start": "python server.py",
        "env_path": "envs/wordle_env/nemo_gym",
        "color": "#76b900",
    },
    "verifiers": {
        "name": "Verifiers",
        "vendor": "@willccbb",
        "sandbox": None,  # in-process — no server
        "port": None,
        "start": None,
        "env_path": "envs/wordle_env/verifiers",
        "color": "#8338ec",
    },
}


def run_islo(args, **kw):
    with tempfile.TemporaryDirectory() as td:
        return subprocess.run([ISLO, *args], cwd=td, check=True, capture_output=True, text=True, **kw)


def provision_one(fw: str, meta: dict) -> dict:
    if meta["sandbox"] is None:
        # In-process: just clone + install locally inside a sandbox for code reference;
        # no server, no share URL.
        return {"framework": fw, **meta, "share_url": None, "status": "in-process"}

    setup_script = f"""set -e
export PATH=$HOME/.local/bin:$PATH
command -v uv >/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1)
export PATH=$HOME/.local/bin:$PATH
cd /workspace/RL_Envs_101/{meta['env_path']}
uv venv .venv >/dev/null 2>&1
. .venv/bin/activate
uv pip install -e . 2>&1 | tail -5
pkill -f 'wordle.*server|server.app|server.py' 2>/dev/null || true
sleep 1
setsid -f bash -c 'cd /workspace/RL_Envs_101/{meta['env_path']} && . .venv/bin/activate && {meta['start']}' </dev/null >/tmp/server.log 2>&1
sleep 8
curl -sI http://localhost:{meta['port']}/ 2>&1 | head -3
"""
    run_islo([
        "use", meta["sandbox"],
        "--source", "github://adithya-s-k/RL_Envs_101",
        "--", "bash", "-c", setup_script,
    ])
    share = run_islo(["share", meta["sandbox"], str(meta["port"]), "--ttl", "24h", "-o", "json"])
    info = json.loads(share.stdout)
    share_url = info.get("url") or info.get("URL")
    return {"framework": fw, **meta, "share_url": share_url, "status": "running"}


def main() -> int:
    CARDS.mkdir(exist_ok=True)
    for fw, meta in FRAMEWORKS.items():
        try:
            card = provision_one(fw, meta)
        except subprocess.CalledProcessError as e:
            print(f"[{fw}] FAILED: {e.stderr}", file=sys.stderr)
            card = {"framework": fw, **meta, "share_url": None, "status": "failed", "error": str(e.stderr)[:500]}
        (CARDS / f"{fw}.json").write_text(json.dumps(card, indent=2))
        print(f"[{fw}] {card.get('share_url') or card.get('status')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
