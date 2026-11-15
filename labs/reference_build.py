"""The hardened build of Mukhallis: every control of the course, switched on (AE-308).

    import reference_build as RB
    controls = RB.hardened()                    # a `controls` dict for M.Agent, M.run_attack, M.run_tasks
    controls = RB.hardened(guard=True)          # the same with the input guardrail of Lab 4.1 in front
    controls = RB.build("egress", "recipients") # only the named controls

Read it after you tried a lab, not before: each function here is one lab's solution. The labs of
Day 4 and the capstone start from it, so that no lab depends on your having finished an earlier one.

    name          lab   what it does
    pins          2.4   refuses a tool whose description no longer matches its approved hash
    sandbox       3.1   duty code: no network, tariff table read-only, paths resolved before the check
    egress        3.2   outbound requests to three hosts only
    recipients    3.2   email only to the registered contact and broker of the case in hand
    tokens        3.3   one exchanged token per call: one audience, one scope, 120 seconds, bound to the case
    split         3.4   the planner sees typed fields of a message, never its text
    guard         4.1   an input classifier in front of text from outside (optional)
    arguments     4.2   schemas and policy rules on tool arguments
    render        4.2   output escaped, images and secrets removed, before the case screen renders it
    approval      4.3   one approval, on email that breaks a rule, with a card a person can judge
    limits        4.4   a cap on model calls and on emails per run
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

import mukhallis as M
import sandbox

HERE = Path(__file__).resolve().parent
ALLOWED_HOSTS = (M.HOST["case"], M.HOST["comms"], M.HOST["rates"])
CURRENCIES = {"SAR", "USD", "EUR", "AED", "CNY"}
HEADER = ("id", "kind", "importer_id", "lang", "cc", "from")
RESTRICTED = {"iban": r"\bSA\d{22}\b", "mobile": r"\+9665\d{8}\b"}
SECRET = r"FANAR-KEY-\w+"


# ── Lab 2.4: pins ────────────────────────────────────────────────────────────────────────────────
def digest(tool: dict) -> str:
    return hashlib.sha256(tool["description"].encode("utf-8")).hexdigest()


PINS = {name: hashlib.sha256(t["description"].encode("utf-8")).hexdigest() for name, t in M.TOOL.items()}


def verify_tools(listing: list[dict]) -> list[str]:
    return [t["name"] for t in listing if PINS.get(t["name"]) != digest(t)]


# ── Lab 3.1: the sandbox policy ──────────────────────────────────────────────────────────────────
def allowed(path, write, tariff, work) -> bool:
    p = os.path.realpath(path)
    under = lambda folder: p.startswith(os.path.realpath(folder) + os.sep)
    return under(work) or (under(tariff) and not write)


def sandbox_policy(work: Path) -> dict:
    return {"network": False, "allowed": lambda p, w: allowed(p, w, sandbox.TARIFF, work)}


# ── Lab 3.2: egress and recipients ───────────────────────────────────────────────────────────────
def egress_allow(host: str) -> bool:
    return host in ALLOWED_HOSTS


def recipients(call) -> list[str]:
    return [a.strip() for a in str(call["args"].get("to", "")).split(",") if a.strip()]


def registered_of(ctx) -> set[str]:
    return {ctx["importer"].get("contact_email"), ctx["importer"].get("broker_email")} - {"", None}


def registered(call, ctx):
    if call["tool"] in ("send_email", "send_case_summary"):
        to = recipients(call)
        if not to or any(a not in registered_of(ctx) for a in to):
            return "a recipient is not registered for this importer"
    return None


# ── Lab 3.3: exchanged tokens ────────────────────────────────────────────────────────────────────
def token_for(call, ctx) -> str:
    tool = M.TOOL[call["tool"]]
    request = {"grant_type": M.Idp.GRANT, "subject_token": ctx["user_token"], "subject_token_type": M.Idp.ACCESS,
               "audience": tool["server"] + "-server", "scope": tool["scope"], "case": ctx["msg_id"]}
    return ctx["world"].idp.token(request, client="mukhallis")["access_token"]


def check_token(claims, tool, args, now, server):
    if claims.get("aud") != server.name + "-server":
        return f"audience {claims.get('aud')} is not {server.name}-server"
    if claims.get("exp", 0) <= now:
        return "the token has expired"
    if M.TOOL[tool]["scope"] not in claims.get("scope", "").split():
        return f"scope {M.TOOL[tool]['scope']} was not granted"
    case = claims.get("case")
    if "msg_id" in args and args["msg_id"] != case:
        return f"the token is bound to {case}, not {args['msg_id']}"
    if "importer_id" in args and (not case or server.world.messages[case]["importer_id"] != args["importer_id"]):
        return f"the token's case does not belong to {args['importer_id']}"
    return None


def setup(world) -> None:
    world.idp.ttl = 120
    for server in world.servers.values():
        server.token_check = check_token


# ── Lab 3.4: the split ───────────────────────────────────────────────────────────────────────────
def validate(fields: dict) -> dict:
    def number(v):
        try:
            return float(v) if float(v) > 0 else None
        except (TypeError, ValueError):
            return None

    match = lambda pattern, v: v if isinstance(v, str) and re.fullmatch(pattern, v) else None
    return {"hs_code": match(r"\d{4}\.\d{2}", fields.get("hs_code")), "value": number(fields.get("value")),
            "currency": fields.get("currency") if fields.get("currency") in CURRENCIES else None,
            "origin": match(r"[A-Z]{2}", fields.get("origin")), "chapter": match(r"\d{2}", fields.get("chapter"))}


def quarantine(message: dict) -> dict:
    return {**{k: message.get(k, "") for k in HEADER}, **validate(M.extract(message))}


# ── Lab 4.1: the input guardrail ─────────────────────────────────────────────────────────────────
_GUARD: dict = {}


def train_guard():
    """A character n-gram classifier trained on the `train` split of data/guardrail_set.jsonl."""
    if "pipe" not in _GUARD:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        rows = [r for r in M.raw("guardrail_set") if r["split"] == "train"]
        pipe = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True),
                             LogisticRegression(C=4.0, max_iter=1000, random_state=308))
        pipe.fit([r["text"] for r in rows], [r["label"] for r in rows])
        _GUARD["pipe"] = pipe
    return _GUARD["pipe"]


def guard_score(text: str) -> float:
    return float(train_guard().predict_proba([text])[0][1])


def input_guard(threshold: float):
    return lambda text, origin: len(text) >= 12 and guard_score(text) >= threshold


# ── Lab 4.2: arguments and output ────────────────────────────────────────────────────────────────
class SendEmail(BaseModel):
    to: str = Field(pattern=r"^[\w.+-]+@[\w-]+(\.[\w-]+)+(\s*,\s*[\w.+-]+@[\w-]+(\.[\w-]+)+)*$")
    subject: str = Field(default="", max_length=120)
    body: str = Field(max_length=2000)


class UpdateCase(BaseModel):
    msg_id: str = Field(pattern=r"^MSG-\d{4}$")
    duty_sar: float = Field(ge=0, le=5_000_000)
    note: str = Field(default="", max_length=200)


class FetchRate(BaseModel):
    currency: Literal["SAR", "USD", "EUR", "AED", "CNY"]
    source_url: Literal["https://rates.gulfbank.example/sar"] = M.RATE_URL


SCHEMAS = {"send_email": SendEmail, "update_case": UpdateCase, "fetch_rate": FetchRate}


def check_schema(call, ctx):
    schema = SCHEMAS.get(call["tool"])
    if schema:
        try:
            schema(**call["args"])
        except ValidationError as err:
            first = err.errors()[0]
            return f"argument {'.'.join(str(p) for p in first['loc'])}: {first['msg']}"
    return None


def check_policy(call, ctx):
    tool, args = call["tool"], call["args"]
    if tool == "release_hold":
        return "a hold is released by an officer, never by the assistant"
    if "msg_id" in args and args["msg_id"] != ctx["msg_id"]:
        return "this is not the case in hand"
    if tool in ("get_importer", "recall", "remember") and args.get("importer_id") != ctx["importer"].get("importer_id"):
        return "this is not the importer of the case in hand"
    if tool == "remember" and re.search(r"@|https?://", str(args.get("note", ""))):
        return "a remembered note may not hold an address or a link"
    return None


def render_safe(text: str) -> str:
    text = re.sub(SECRET, "[removed]", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "[image removed]", text)
    return html.escape(text)


# ── Lab 4.3: one approval ────────────────────────────────────────────────────────────────────────
def data_found(text: str) -> list[str]:
    return sorted(name for name, pattern in RESTRICTED.items() if re.search(pattern, text))


def needs_approval(call, ctx) -> bool:
    if call["tool"] not in ("send_email", "send_case_summary"):
        return False
    return any(a not in registered_of(ctx) for a in recipients(call)) or bool(data_found(str(call["args"].get("body", "")))) \
        or call["tool"] == "send_case_summary"


def card(call, ctx) -> dict:
    to = recipients(call)
    return {"action": "send an email" if call["tool"] == "send_email" else "send a whole case summary",
            "case": ctx["msg_id"], "importer": ctx["importer"].get("company", ""), "to": to,
            "registered": all(a in registered_of(ctx) for a in to), "registered_addresses": sorted(registered_of(ctx)),
            "data_found": data_found(str(call["args"].get("body", ""))) + (["the importer record"] if call["tool"] == "send_case_summary" else []),
            "first_lines": str(call["args"].get("body", ""))[:160]}


CONTROLS = ("pins", "sandbox", "egress", "recipients", "tokens", "split", "arguments", "render", "approval", "limits")


def build(*names: str, guard: bool = False, threshold: float | None = None, approver=None) -> dict:
    """A controls dict with the named controls on."""
    c: dict = {"before_tool": []}
    if "pins" in names:
        c["verify_tools"] = verify_tools
    if "sandbox" in names:
        work = sandbox.workdir("agent")
        c.update(work=work, sandbox=sandbox_policy(work))
    if "egress" in names:
        c["egress_allow"] = egress_allow
    if "arguments" in names:
        c["before_tool"] += [check_schema, check_policy]
    if "recipients" in names and "approval" not in names:
        c["before_tool"].append(registered)
    if "tokens" in names:
        c.update(setup=setup, token_for=token_for)
    if "split" in names:
        c["quarantine"] = quarantine
    if "render" in names:
        c["render"] = render_safe
    if "approval" in names:  # the approval takes the place of the flat refusal: a person decides the flagged emails
        c.update(needs_approval=needs_approval, card=card, approver=approver or M.Approver())
    if "limits" in names:
        c["limits"] = {"max_calls": 14, "max_emails": 2}
    if guard:
        if threshold is None:
            threshold = json.loads((HERE / "data" / "reference" / "d4_1_report.json").read_text(encoding="utf-8"))["threshold"]
        c["input_guard"] = input_guard(threshold)
    return c


def hardened(guard: bool = False, approver=None) -> dict:
    return build(*CONTROLS, guard=guard, approver=approver)
