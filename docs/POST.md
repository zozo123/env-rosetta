# env-rosetta: one Wordle env, four RL frameworks, islo.dev sandboxes

*Yossi Eliaz · May 2026 · demo*

**TL;DR.** [@adithya-s-k](https://github.com/adithya-s-k)'s [RL_Envs_101](https://github.com/adithya-s-k/FineEnvs) (since renamed FineEnvs) implements the same Wordle env in several RL frameworks. This demo takes four of them, OpenEnv (Meta), ORS, NeMo Gym (NVIDIA) and Verifiers (in-process), and runs each framework server in its own [islo.dev](https://islo.dev) sandbox instead of the HuggingFace Spaces that upstream deploys to. It was a single run on 2026-05-11: OpenEnv and ORS ran, NeMo Gym did not finish provisioning, and Verifiers has no server. The sandboxes have since been shut down.

Disclosure: the author works on islo.dev at Incredibuild.

## Why one sandbox per server

Per-rollout sandbox isolation helps when:
- you're running **K parallel rollouts** during a training step and they each mutate state (tools, files, scratch dirs);
- you need to **shell into a stuck env** for debugging;
- you want a **fresh start per trial** so a misbehaving env in trial T doesn't affect trial T+1.

Here each framework server runs in its own islo.dev sandbox: `islo use <name> --source github://...` creates the sandbox and starts the server, and `islo share <name> <port>` gives it a temporary public URL that a rollout client can call. This demo only sets up that deployment; it does not run parallel rollouts or training.

## Tier 2 (not built): porting the Jupyter env from E2B to Islo

Adithya's Jupyter agent env executes real Python code inside a sandbox. In his repo (as of upstream commit `41c0463`) that sandbox is **E2B**: the four framework ports each `from e2b_code_interpreter import Sandbox` and use it through a thin `e2b_sandbox.py` wrapper.

Swapping E2B for Islo there is not mechanical. You'd:
1. Write an `IsloSandbox` class with the same surface as `E2BSandbox`: `run_code(str)`, `kill()`, persistent kernel state across calls, image capture for matplotlib (Adithya's `_SETUP_CODE` patches `plt.show()` to route through IPython).
2. The IsloSandbox would shell out to `islo use <ephemeral-name> --source ... -- bash -c '<python -c …>'` per call, OR keep a single sandbox up per session and execute over a small RPC. Latter is closer to E2B's semantics.
3. Update each framework's `envs/jupyter_env/<framework>/e2b_sandbox.py` (or write a parallel `islo_sandbox.py` and a flag).
4. Verify Jupyter notebook semantics: variables persist between calls in the same sandbox.

Tier 2 would port the Jupyter env from E2B to Islo; it is not built. The Wordle demo in this repo only covers the deployment shape.

## Honest framing

- The four framework cards on the page link to the **same Wordle game logic**, exposed through each framework's idioms. The judging step in Adithya's repo is "did the LLM solve the puzzle." This repo has no code that calls an LLM; each card shows the same **scripted example transcript** (not an LLM rollout), written by `bin/rollout.py`.
- One of the sandboxes (NeMo Gym) hit a transient `islo` exec-stream error during initial provisioning; its card still records `provisioning`. OpenEnv and ORS ran; their 24-hour share links have expired.
- Verifiers doesn't have a server in this env — it's an in-process Python module. No share URL, no sandbox. The card shows code + transcript only.

## Credits

- Envs + framework adapters: [@adithya-s-k, RL_Envs_101 / FineEnvs](https://github.com/adithya-s-k/FineEnvs)
- Sandbox infra: [islo.dev](https://islo.dev)
- Related demos: [unity-loop](https://github.com/zozo123/unity-loop), [pokeloop](https://github.com/zozo123/pokeloop), [meta-harness-on-islo](https://github.com/zozo123/meta-harness-on-islo)
