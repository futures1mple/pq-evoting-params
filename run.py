"""
Run the lattice estimator on one problem instance under one cost model.

usage: python run.py <problem_id> <model>      model in {core292, core265, matzov}
Writes results/<problem_id>__<model>.json and logs/<problem_id>__<model>.log
"""
import sys, json, time, io, contextlib, subprocess, os
from math import log2, sqrt
sys.path.insert(0, os.environ.get("LE_PATH", "lattice-estimator"))
from estimator import LWE, SIS, NTRU, ND, RC
from estimator.reduction import ADPS16
from params import PROBLEMS

MODELS = {
    "core292": ADPS16(mode="classical"),   # 2^(0.292 beta)
    "core265": ADPS16(mode="quantum"),     # 2^(0.265 beta)
    "matzov":  RC.MATZOV,
}

def dist(spec):
    t, a = spec
    if t == "DG": return ND.DiscreteGaussian(a)
    if t == "T":  return ND.Uniform(-1, 1)
    if t == "B":  return ND.Uniform(0, 1)
    if t == "CB": return ND.CenteredBinomial(a)
    if t == "U":  return ND.Uniform(*a) if a else None
    raise ValueError(t)

def build(p):
    if p["kind"] == "LWE":
        Xs = ND.UniformMod(p["q"]) if p["Xs"][0] == "U" and p["Xs"][1] is None else dist(p["Xs"])
        return LWE.Parameters(n=p["n"], q=p["q"], Xs=Xs, Xe=dist(p["Xe"]), m=p["m"], tag=p["id"])
    if p["kind"] == "NTRU":
        return NTRU.Parameters(n=p["n"], q=p["q"], Xs=dist(p["Xs"]), Xe=dist(p["Xe"]), tag=p["id"])
    if p["kind"] == "SIS":
        norm = 2 if p["norm"] == 2 else float("inf")
        from sage.all import oo
        return SIS.Parameters(n=p["n"], q=p["q"], length_bound=p["beta"], m=p["m"],
                              norm=2 if p["norm"] == 2 else oo, tag=p["id"])

def to_jsonable(cost):
    out = {}
    for k, v in dict(cost).items():
        try:
            fv = float(v)
            out[k] = fv
            if k in ("rop", "red", "mem", "guess", "svp") and fv > 0:
                out[k + "_log2"] = log2(fv) if fv != float("inf") else float("inf")
        except Exception:
            out[k] = str(v)
    return out

def trivial_check(p):
    """Rule R4: binding is broken by linear algebra alone if the bound exceeds the norm
    ~ q*sqrt(rows/12) of kernel vectors (x, -A'x) with x a unit vector (l2), or q/2 (l_inf)."""
    if p["kind"] != "SIS":
        return None
    q = p["q"]
    la = q * sqrt(p["n"] / 12) if p["norm"] == 2 else (q - 1) / 2
    return {"beta_log2": log2(p["beta"]), "q_log2": log2(q),
            "linear_algebra_norm_log2": log2(la), "trivial": p["beta"] >= la}

def main(pid, model):
    p = next(x for x in PROBLEMS if x["id"] == pid)
    params = build(p)
    est = {"LWE": LWE, "SIS": SIS, "NTRU": NTRU}[p["kind"]]
    buf = io.StringIO()
    t0 = time.time()
    with contextlib.redirect_stdout(buf):
        res = est.estimate(params, red_cost_model=MODELS[model], jobs=1)
    dt = time.time() - t0
    attacks = {k: to_jsonable(v) for k, v in res.items()}
    finite = [a["rop_log2"] for a in attacks.values() if "rop_log2" in a]
    best = min(finite) if finite else None
    best_attack = min(((a["rop_log2"], k) for k, a in attacks.items() if "rop_log2" in a), default=(None, None))[1]
    commit = subprocess.run(["git", "-C", os.environ.get("LE_PATH", "lattice-estimator"), "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    rec = {"id": pid, "model": model, "estimator_commit": commit, "params": repr(params),
           "problem": {k: v for k, v in p.items()}, "attacks": attacks,
           "min_rop_log2": best, "best_attack": best_attack, "seconds": round(dt, 1),
           "trivial_check": trivial_check(p)}
    RD = os.environ.get("OUT_DIR", "results"); LD = os.environ.get("LOG_DIR", "logs")
    os.makedirs(RD, exist_ok=True); os.makedirs(LD, exist_ok=True)
    tag = f"{pid}__{model}"
    with open(f"{RD}/{tag}.json", "w") as f:
        json.dump(rec, f, indent=1, default=str)
    with open(f"{LD}/{tag}.log", "w") as f:
        f.write(f"# estimator commit {commit}\n# {repr(params)}\n# model {model}\n")
        f.write(buf.getvalue())
        for k, v in res.items():
            f.write(f"{k:20s} :: {v!r}\n")
    print(tag, best, best_attack, f"{dt:.0f}s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
