"""The duty-code runner of Mukhallis and its policy layer.

    import sandbox
    out = sandbox.run(code, policy=None, world=world)          # as found: no restriction
    out = sandbox.run(code, policy={"network": False, "allowed": allowed}, world=world)

The code gets these names: json, math, csv, os, Path, TARIFF (the tariff folder), WORK (its work
folder), http_post(url, data) and must leave its answer in `result`.

What this is and is not. The policy is enforced with a Python audit hook in the same process: every
file open made by the code is passed to `allowed(path, write)`, and `http_post` is refused when the
network is off. It teaches the three decisions of a real sandbox (no network, read-only mounts,
resolve a path before you check it) and stands in for the flags of a container runtime. It is not a
security boundary: in production the same policy is given to a container or a user-space kernel.
Real sockets and subprocesses are refused in every mode, so no payload of the labs leaves the
notebook.
"""

from __future__ import annotations

import csv
import json
import math
import os
import shutil
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARIFF = HERE / "data" / "tariff"
_state = {"thread": None, "policy": None}
_DENY = ("socket.connect", "socket.getaddrinfo", "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn")


def _hook(event, args):
    if _state["thread"] != threading.get_ident():
        return
    if event in _DENY:
        raise PermissionError(f"sandbox: {event} is refused in the labs")
    policy = _state["policy"]
    if event == "open" and policy is not None and isinstance(args[0], (str, bytes, os.PathLike)):
        path, mode, flags = os.fsdecode(args[0]), args[1], args[2]
        write = bool(set(mode or "") & set("wax+")) if mode else bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        if not policy["allowed"](path, write):
            raise PermissionError(f"sandbox: {'write to' if write else 'read of'} {Path(path).name} denied")


sys.addaudithook(_hook)


def workdir(name: str) -> Path:
    """A fresh, empty work folder for one lab: labs/artifacts/<name>/work."""
    work = HERE / "artifacts" / name / "work"
    if work.exists():
        for child in work.iterdir():  # a link is removed as a link, never followed
            if child.is_symlink() or getattr(child, "is_junction", lambda: False)():
                os.unlink(child) if child.is_symlink() else os.rmdir(child)
        shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True, exist_ok=True)
    return work


def plant_link(work: Path, target: Path) -> Path:
    """Leaves a link `ref` in the work folder that points at `target`: the planted escape. Give it a copy, never the course data."""
    link = work / "ref"
    if not link.exists():
        try:
            os.symlink(target, link, target_is_directory=True)
        except OSError:  # Windows without the right to create symbolic links: a junction does the same
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
    return link


def run(code: str, policy: dict | None = None, world=None, work: Path | None = None, tariff: Path | None = None) -> dict:
    work = work or workdir("default")

    def http_post(url, data):
        if policy is not None and not policy.get("network", False):
            raise PermissionError("sandbox: no network")
        if world is None:
            raise PermissionError("sandbox: no gateway")
        from urllib.parse import urlparse
        return world.net(urlparse(url).netloc, urlparse(url).path or "/", {"data": str(data)}, via="code")

    def _import(name, *a, **k):
        if name.split(".")[0] not in ("json", "math", "csv", "os", "pathlib", "base64", "decimal"):
            raise ImportError(f"sandbox: import of {name} is not offered")
        return __import__(name, *a, **k)

    builtins = dict(__builtins__) if isinstance(__builtins__, dict) else dict(vars(__builtins__))
    builtins["__import__"] = _import
    env = {"__builtins__": builtins, "json": json, "math": math, "csv": csv, "os": os, "Path": Path,
           "TARIFF": tariff or TARIFF, "WORK": work, "http_post": http_post, "result": None}
    _state.update(thread=threading.get_ident(), policy=policy)
    try:
        exec(compile(code, "<duty code>", "exec"), env)  # noqa: S102 - the subject of the lab
        out = {"result": env.get("result")}
    except Exception as exc:  # noqa: BLE001 - reported to the caller
        out = {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        _state.update(thread=None, policy=None)
    return out
