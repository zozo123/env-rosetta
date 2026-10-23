# env-rosetta

A May 2026 demo for people comparing RL environment frameworks: one Wordle env from [@adithya-s-k](https://github.com/adithya-s-k)'s [RL_Envs_101](https://github.com/adithya-s-k/FineEnvs) (since renamed FineEnvs) shown in four frameworks, with two of the framework servers run in short-lived [islo.dev](https://islo.dev/) sandboxes. The sandboxes are gone and the transcripts are scripted.

**Project page:** https://zozo123.github.io/env-rosetta-page/ · **Writeup:** [`docs/POST.md`](./docs/POST.md) · **By** [Yossi Eliaz](https://zozo123.github.io/)

---

## What this is

Adithya's RL_Envs_101 reimplements the same environments across six RL frameworks as a "Rosetta stone" for RL env design. This repo takes the Wordle env in four of those frameworks and gives each server-based one its own islo.dev sandbox, instead of the HuggingFace Spaces that upstream deploys to.

| Sandbox | Framework | Server style | Status on 2026-05-11 | Code excerpt |
|---|---|---|---|---|
| `rosetta-openenv` | [OpenEnv](https://github.com/meta-pytorch/OpenEnv) (Meta) | FastAPI + MCP | ran | [`openenv/server/app.py`](https://github.com/adithya-s-k/FineEnvs/blob/41c04630fbb3aba001c9a6ab656893e6ac2a0961/envs/wordle_env/openenv/server/app.py) |
| `rosetta-ors` | [ORS](https://github.com/openreward/openreward) (Open Reward Standard) | HTTP | ran | [`ors/server.py`](https://github.com/adithya-s-k/FineEnvs/blob/41c04630fbb3aba001c9a6ab656893e6ac2a0961/envs/wordle_env/ors/server.py) |
| `rosetta-nemo-gym` | [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) (NVIDIA) | HTTP | did not finish provisioning | [`nemo_gym/server.py`](https://github.com/adithya-s-k/FineEnvs/blob/41c04630fbb3aba001c9a6ab656893e6ac2a0961/envs/wordle_env/nemo_gym/server.py) |
| (none) | [Verifiers](https://github.com/PrimeIntellect-ai/verifiers) | In-process (no server) | in-process, no sandbox | [`verifiers/env.py`](https://github.com/adithya-s-k/FineEnvs/blob/41c04630fbb3aba001c9a6ab656893e6ac2a0961/envs/wordle_env/verifiers/env.py) |

**Status:** this was a single run on 2026-05-11. The sandboxes were temporary (24-hour share links) and have been shut down. OpenEnv and ORS ran; NeMo Gym did not finish provisioning; Verifiers runs in-process. The files in [`cards/`](./cards) record that run's sandbox names and status: their `share_url` values no longer resolve, and their `rollout` transcripts are scripted examples, not LLM rollouts.

Each server exposes the same game tools (`guess(word)`, `get_history()`) in its own framework's idiom. The code excerpt links are pinned to upstream commit `41c0463`, which the excerpts in `cards/` match. Upstream has since moved the Wordle env to `00-environments-101/envs/wordle/`, so `bin/provision.py` would need its paths updated before it could run again.

## Why one sandbox per server

Each framework server runs in its own islo.dev sandbox, so each one is an isolated machine you can shell into, restart, or recreate without touching the others. That is the shape you would want if parallel rollouts must not share state. This demo only shows the deployment; it does not run parallel rollouts or training.

## Commands

```bash
bin/env-rosetta provision    # spawn 3 islo sandboxes (Verifiers runs in-process), install deps, start servers, share ports
bin/env-rosetta rollout      # write a scripted example transcript into each card (no LLM call, no network)
bin/env-rosetta page         # bundle cards/*.json into ../env-rosetta-page/cards.json
bin/env-rosetta demo         # offline: fill cards/*.json with placeholder data
```

## Tier 2 (not built): the Jupyter env on islo.dev

Upstream's Jupyter agent env runs Python through `e2b-code-interpreter` (E2B). Tier 2 would port that env from E2B to Islo: an `IsloSandbox` class with the same `run_code` interface as `E2BSandbox`, wired through `envs/jupyter_env/<framework>/e2b_sandbox.py` in all four frameworks. It is not built. The steps are sketched in [`docs/POST.md`](./docs/POST.md#tier-2-not-built-porting-the-jupyter-env-from-e2b-to-islo).

## Credits

- Envs, framework adapters and the Rosetta-stone idea: [@adithya-s-k](https://github.com/adithya-s-k), [RL_Envs_101 / FineEnvs](https://github.com/adithya-s-k/FineEnvs)
- Frameworks: OpenEnv, ORS, NeMo Gym, Verifiers (linked above)
- Sandbox infra: [islo.dev](https://islo.dev/)
- Related demos: [unity-loop](https://github.com/zozo123/unity-loop) · [pokeloop](https://github.com/zozo123/pokeloop) · [meta-harness-on-islo](https://github.com/zozo123/meta-harness-on-islo)

Disclosure: the author works on islo.dev at Incredibuild.

## License

This repo's own code is MIT ([`LICENSE`](./LICENSE)). Code excerpts © adithya-s-k, RL_Envs_101, Apache-2.0.
