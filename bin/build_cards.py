"""Bundle cards/*.json into env-rosetta-page/cards.json for the gh-pages site."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"
PAGE = ROOT.parent / "env-rosetta-page"
OUT = PAGE / "cards.json"

ORDER = ["openenv", "ors", "nemo_gym", "verifiers"]

bundle = []
for fw in ORDER:
    p = CARDS / f"{fw}.json"
    if not p.exists():
        continue
    bundle.append(json.loads(p.read_text()))

OUT.write_text(json.dumps(bundle, indent=2))
print(f"wrote {OUT} ({len(bundle)} cards)")
