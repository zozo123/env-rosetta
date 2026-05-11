# env-rosetta — the per-sandbox Rosetta stone for RL envs

**TL;DR.** Four parallel [islo.dev](https://islo.dev) sandboxes, each running a different RL framework's port of [@adithya-s-k](https://github.com/adithya-s-k)'s Wordle env from [RL_Envs_101](https://github.com/adithya-s-k/RL_Envs_101). Same env logic, four dialects: OpenEnv (Meta), ORS, NeMo Gym (NVIDIA), Verifiers (in-process). HF Spaces is the reference deployment target in Adithya's repo; this is the islo-cold-per-trial-sandbox alternative.

## Why the swap matters

You want per-rollout sandbox isolation when:
- you're running **K parallel rollouts** during a training step and they each mutate state (tools, files, scratch dirs);
- you need to **`ssh` into a stuck env** for debugging;
- you want a **cold start per trial** so a misbehaving env in trial T doesn't poison trial T+1.

HF Spaces is one shared service per app — perfect for a static demo, less so for RL training-time env hosting. islo `use <name> --source github://...` spins a cold worker in seconds; `islo share <name> <port>` gives you a public URL that the rollout client (or the entire training process) can hit.

## Tier 2: Jupyter env — "islo replaces E2B"

Adithya's Jupyter agent env executes real Python code inside a sandbox. In his repo that sandbox is **E2B** — the four framework ports each `from e2b_code_interpreter import Sandbox` and use it through a thin `e2b_sandbox.py` wrapper.

Swapping E2B for islo there is not mechanical. You'd:
1. Write an `IsloSandbox` class with the same surface as `E2BSandbox`: `run_code(str)`, `kill()`, persistent kernel state across calls, image capture for matplotlib (Adithya's `_SETUP_CODE` patches `plt.show()` to route through IPython).
2. The IsloSandbox would shell out to `islo use <ephemeral-name> --source ... -- bash -c '<python -c …>'` per call, OR keep a single sandbox up per session and execute over a small RPC. Latter is closer to E2B's semantics.
3. Update each framework's `envs/jupyter_env/<framework>/e2b_sandbox.py` (or write a parallel `islo_sandbox.py` and a flag).
4. Verify Jupyter notebook semantics: variables persist between calls in the same sandbox.

That's the real "islo replaces E2B" demo. The Wordle rosetta in this repo proves the deployment shape works; Tier 2 makes the value clear.

## Honest framing

- The four framework cards on the page link to the **same Wordle game logic**, exposed through each framework's idioms. The judging step in Adithya's repo is "did the LLM solve the puzzle." We don't run rollouts on every page load — that needs API keys, money, and time. Cards show **canned transcripts** from a single successful rollout per framework.
- One of the sandboxes (NeMo Gym) hit a transient `islo` exec-stream error during initial provisioning. It will show `warming` on the page until a retry succeeds. The other three (OpenEnv, ORS, Verifiers in-process) are live.
- Verifiers doesn't have a server in this env — it's an in-process Python module. No share URL, no sandbox. The card shows code + transcript only.

## Credits

- Envs + framework adapters: [@adithya-s-k/RL_Envs_101](https://github.com/adithya-s-k/RL_Envs_101)
- Sandbox infra: [islo.dev](https://islo.dev)
- Sibling: [unity-loop](https://github.com/zozo123/unity-loop), [pokeloop](https://github.com/zozo123/pokeloop), [meta-harness-on-islo](https://github.com/zozo123/meta-harness-on-islo)
