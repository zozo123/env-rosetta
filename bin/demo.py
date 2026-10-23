"""Offline walkthrough — fills cards/*.json with placeholder data and the scripted example transcript, no network."""
import json
from pathlib import Path

from rollout import run_scripted

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"

FRAMEWORKS = {
    "openenv":   {"name": "OpenEnv",   "vendor": "Meta",                 "color": "#3a86ff", "sandbox": "rosetta-openenv"},
    "ors":       {"name": "ORS",       "vendor": "Open Reward Standard", "color": "#ff006e", "sandbox": "rosetta-ors"},
    "nemo_gym":  {"name": "NeMo Gym",  "vendor": "NVIDIA",               "color": "#76b900", "sandbox": "rosetta-nemo-gym"},
    "verifiers": {"name": "Verifiers", "vendor": "@willccbb",            "color": "#8338ec", "sandbox": None},
}

CARDS.mkdir(exist_ok=True)

print("env-rosetta · demo mode (no network)")
print()
for fw, meta in FRAMEWORKS.items():
    card = {
        "framework": fw,
        **meta,
        "share_url": None if meta["sandbox"] is None else f"https://example-{fw}.share.islo.dev",
        "status": "demo",
        "rollout": run_scripted(fw),
    }
    (CARDS / f"{fw}.json").write_text(json.dumps(card, indent=2))
    print(f"  ✓ {meta['name']:<14} → cards/{fw}.json")
print()
print("Next: bin/env-rosetta page  (bundles cards into env-rosetta-page/cards.json)")
