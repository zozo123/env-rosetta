"""Write a scripted example transcript into each framework card.

This is not an LLM rollout: no model is called and no server is contacted.
Every card gets the same hand-written four-guess game against the target
word 'paint', with feedback that matches that target.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"

TARGET = "paint"
SCRIPTED = {
    "guesses": [
        ("crane", "⬛⬛🟨🟩⬛", "5 guesses remaining"),
        ("share", "⬛⬛🟨⬛⬛", "4 guesses remaining"),
        ("alert", "🟨⬛⬛⬛🟩", "3 guesses remaining"),
        ("paint", "🟩🟩🟩🟩🟩", f"WIN — '{TARGET}'"),
    ],
}


def run_scripted(fw: str) -> dict:
    lines = [f"# scripted example, not a real rollout ({fw})"]
    for word, feedback, status in SCRIPTED["guesses"]:
        lines.append(f">  guess('{word}')  → {feedback}  ({status})")
    return {"transcript": "\n".join(lines), "scripted": True, "won": True, "guesses_used": 4}


def main() -> int:
    CARDS.mkdir(exist_ok=True)
    for fw in ("openenv", "ors", "nemo_gym", "verifiers"):
        card_path = CARDS / f"{fw}.json"
        card: dict = json.loads(card_path.read_text()) if card_path.exists() else {"framework": fw}
        card["rollout"] = run_scripted(fw)
        card_path.write_text(json.dumps(card, indent=2))
        print(f"[{fw}] scripted example transcript written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
