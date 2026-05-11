# HN post — Show HN: env-rosetta — Wordle env across 4 RL frameworks, 4 islo.dev sandboxes

## Title (≤80 chars)
Show HN: Same Wordle env across 4 RL frameworks, each in its own islo.dev sandbox

## URL
https://zozo123.github.io/env-rosetta-page/

## Body (markdown)

`env-rosetta` is a Rosetta stone for RL environments — the same Wordle env reimplemented across **OpenEnv (Meta)**, **ORS (Open Reward Standard)**, **NeMo Gym (NVIDIA)**, and **Verifiers**, each running in its own [islo.dev](https://islo.dev) sandbox. Four cards, four framework dialects, side by side.

This is a thin layer on top of [@adithya-s-k](https://github.com/adithya-s-k)'s excellent [RL_Envs_101](https://github.com/adithya-s-k/RL_Envs_101) — he wrote the env code six times in six frameworks; we took four of them and swapped the HuggingFace Spaces deployment target for islo cold-per-trial sandboxes. The provisioner is literally:

```
islo use rosetta-openenv \
  --source github://adithya-s-k/RL_Envs_101 \
  -- bash -c 'cd envs/wordle_env/openenv && uv venv .venv && . .venv/bin/activate \
              && uv pip install -e . \
              && setsid -f uvicorn server.app:app --host 0.0.0.0 --port 8080'
islo share rosetta-openenv 8080
```

…repeated three more times with the framework-specific entry point.

**Why per-sandbox.** HF Spaces is fine for static demos but you can't run K parallel rollouts cleanly, you can't `ssh` into one to debug a hung env, and you don't get fresh per-trial state. Cold per-rollout sandboxes are the right shape for RL training-time env hosting; this is a tiny POC of that.

**What's not in this POC.** Adithya's *Jupyter agent* env hard-depends on `e2b-code-interpreter` for real Python execution. Swapping E2B → islo there isn't a one-line change — it's writing an `IsloSandbox` class that matches the `E2BSandbox.run_code` API, plumbed through `envs/jupyter_env/<framework>/e2b_sandbox.py` in 4 frameworks. That's the actual "islo replaces E2B" story and it's Tier 2.

Live page: https://zozo123.github.io/env-rosetta-page/
Repo: https://github.com/zozo123/env-rosetta

Sibling demo from this session: [unity-loop](https://github.com/zozo123/unity-loop) — Claude-vision tournament over Unity WebGL variants on parallel islo sandboxes.

Credits: @adithya-s-k for the envs and the multi-framework Rosetta-stone idea; islo.dev for the sandbox infra; the `RL_Envs_101` skill (`npx skills add adithya-s-k/RL_Envs_101`) is what generates new framework adapters in this shape.
