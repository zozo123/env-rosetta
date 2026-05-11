# env-rosetta

**The same Wordle env, four RL frameworks, four parallel [islo.dev](https://islo.dev/) sandboxes.**

> **Project page:** https://zozo123.github.io/env-rosetta-page/
>
> **Writeup:** [`docs/POST.md`](./docs/POST.md)
>
> **Inspired by:** [@adithya_s_k](https://x.com/adithya_s_k)'s [RL_Envs_101](https://github.com/adithya-s-k/RL_Envs_101) — same env reimplemented across 6 frameworks as a "Rosetta stone" for RL env design. This is that Rosetta stone hosted **per-sandbox** on islo.dev instead of one shared HuggingFace Space.
>
> **Sibling:** [unity-loop](https://github.com/zozo123/unity-loop) (Claude-vision tournament over Unity WebGL variants on islo).

---

## What this is

Four islo.dev sandboxes. Each runs Adithya's Wordle env in a different RL framework dialect:

| Sandbox | Framework | Server style | Live URL |
|---|---|---|---|
| `rosetta-openenv` | [OpenEnv](https://github.com/meta-pytorch/OpenEnv) (Meta) | FastAPI + MCP | `cards/openenv.json#share_url` |
| `rosetta-ors` | [ORS](https://github.com/openreward/openreward) (Open Reward Standard) | HTTP | `cards/ors.json#share_url` |
| `rosetta-nemo-gym` | [NeMo Gym](https://github.com/NVIDIA/NeMo-RL) (NVIDIA) | HTTP | `cards/nemo_gym.json#share_url` |
| (in-process) | [Verifiers](https://github.com/willccbb/verifiers) | In-process (no server) | rollout transcript only |

The same MCP/HTTP shape — `guess(word)`, `get_history()`, `reset_game()` — exposed by every server. Same Wordle word every time you click in (seeded per session). Different framework idioms behind the curtain.

## Why islo.dev for this

Adithya's reference deployments live on HuggingFace Spaces (one Space per framework). HF Spaces is fine for static demos but you don't get a fresh per-trial sandbox, you can't `ssh` into one, and you can't run parallel rollouts without sharing state. **islo.dev gives you cold per-rollout sandboxes** — same code, but you can spin K parallel workers, each isolated, each a one-line provision.

## Quick start

```bash
bin/env-rosetta provision    # spawn 4 islo sandboxes, install deps, start each server, share ports
bin/env-rosetta rollout      # run one LLM rollout against each framework, capture transcripts
bin/env-rosetta page         # update cards/*.json (which the gh-pages site reads)
```

Or just look at [`cards/`](./cards) — each framework's metadata, share URL, sample code, and a recorded rollout transcript are versioned there.

## Tier 2 — Jupyter env (the real "islo replaces E2B" story)

Adithya's Jupyter agent env uses `e2b-code-interpreter` for real Python code execution. Porting that to islo is a separate workstream — write an `IsloSandbox` class with the same `run_code` interface as `E2BSandbox`, plumb it through `envs/jupyter_env/<framework>/e2b_sandbox.py` in all 4 frameworks. Sketched in [`docs/POST.md#tier-2`](./docs/POST.md#tier-2-jupyter-env--islo-replaces-e2b). The Wordle rosetta in this repo is the foundation; Tier 2 is the killer demo.

## Credits

- Envs and framework adapters — [@adithya-s-k](https://github.com/adithya-s-k/RL_Envs_101)
- Sandbox infra — [islo.dev](https://islo.dev/)
- Pattern — [unity-loop](https://github.com/zozo123/unity-loop) · [pokeloop](https://github.com/zozo123/pokeloop) · [meta-harness-on-islo](https://github.com/zozo123/meta-harness-on-islo)
- Movie — [agentreel](https://github.com/islo-labs/agentreel)

MIT.
