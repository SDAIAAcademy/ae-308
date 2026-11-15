# %% [markdown]
# # Setup check · before Day 1
#
# Run every cell once. Each prints a tick or says what is missing. Nothing here downloads a model
# and no key is needed.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-308.git"
    if not Path("/content/ae-308").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-308"], check=True)
    os.chdir("/content/ae-308/labs")
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

print("Python", sys.version.split()[0])
assert sys.version_info >= (3, 11), "Python 3.11 or later is needed"

# %% [markdown]
# ## 1 · The libraries and the data

# %%
import pydantic
import sklearn

import fanar as U
import mukhallis as M

print("scikit-learn", sklearn.__version__, "| pydantic", pydantic.VERSION)
world = M.World()
U.check(len(world.importers) == 400 and len(world.messages) == 200 and len(M.tasks()) == 50, "400 importer records, 200 emails and invoices, 50 benign tasks")
U.check(len(M.attacks()) == 30 and len(U.jsonl("guardrail_set.jsonl")) == 640, "30 starter attacks and 640 guardrail texts")

# %% [markdown]
# ## 2 · The agent runs one task

# %%
task = M.tasks(1)[0]
run = M.Agent(world).run(task["text"])
run.show(100)
print("\nmodel:", run.model)
U.check(M.grade(task, run, world), "the first benign task passes")

# %% [markdown]
# ## 3 · Links in a work folder (Lab 3.1)
#
# Lab 3.1 plants a link inside a work folder. On Windows the kit falls back to a directory junction
# when symbolic links are not allowed.

# %%
import sandbox

work = sandbox.workdir("setup_check")
target = U.ART / "setup_check" / "target"
target.mkdir(parents=True, exist_ok=True)
(target / "hello.txt").write_text("hello", encoding="utf-8")
link = sandbox.plant_link(work, target)
U.check((link / "hello.txt").read_text(encoding="utf-8") == "hello" and os.path.realpath(link) == os.path.realpath(target),
        "a link can be created and resolved")
sandbox.workdir("setup_check")

# %% [markdown]
# ## 4 · Optional: a free hosted model
#
# The labs default to a scripted stand-in model, so that everyone gets the same runs. To try a free
# hosted open-weight model, set `MUKHALLIS_MODEL=hosted` and `OPENROUTER_API_KEY` before starting
# Jupyter (in Colab: the Secrets panel, then `os.environ[...]`). Use it with the synthetic data of
# this course only. If the call fails, the stand-in finishes the run and the model line says so.

# %%
if os.environ.get("MUKHALLIS_MODEL") == "hosted":
    w = M.World()
    r = M.Agent(w).run(M.tasks(1)[0]["text"])
    print("model:", r.model, "| calls:", r.calls)
else:
    print("the stand-in model is in use: nothing to check")
print("\nSetup complete.")
