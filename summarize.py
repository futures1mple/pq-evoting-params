"""Collect results/*.json into results/summary.csv and results/summary.md."""
import json, glob, csv, os
from math import isinf
from params import PROBLEMS

MODELS = ["core292", "core265", "matzov"]
PRIMAL = {"usvp", "bdd", "bdd_hybrid", "bdd_mitm_hybrid", "dsd"}

def fmt(x):
    if x is None: return "n/a"
    if isinf(x): return "inf"
    return f"{x:.1f}"

rows = []
for p in PROBLEMS:
    r = {"id": p["id"], "scheme": p["scheme"], "role": p["role"], "component": p["component"],
         "variant": p["variant"], "claimed": p["claimed"], "kind": p["kind"]}
    for m in MODELS:
        f = f"results/{p['id']}__{m}.json"
        if os.path.exists(f):
            j = json.load(open(f))
            r[m] = j["min_rop_log2"]; r[m + "_attack"] = j["best_attack"]
            prim = [a["rop_log2"] for k, a in j["attacks"].items() if k in PRIMAL and "rop_log2" in a]
            r[m + "_primal"] = min(prim) if prim else None
            tc = j.get("trivial_check")
            if tc: r["beta_log2"] = tc["beta_log2"]; r["q_log2"] = tc["q_log2"]; r["trivial"] = tc["trivial"]
            r["commit"] = j["estimator_commit"][:7]
        else:
            r[m] = None
    rows.append(r)

keys = ["id", "scheme", "role", "component", "variant", "kind", "claimed"] + \
       sum([[m, m + "_attack", m + "_primal"] for m in MODELS], []) + ["beta_log2", "q_log2", "trivial", "commit"]
with open("results/summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

with open("results/summary.md", "w") as f:
    f.write("| scheme | role | component | variant | claimed | 0.292b | 0.265b | MATZOV | best attack (MATZOV) | note |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        note = ""
        if r.get("trivial"): note = f"beta=2^{r['beta_log2']:.1f} above the linear-algebra norm (rule R4): trivial"
        elif r["kind"] == "SIS" and r.get("core292") is not None and isinf(r["core292"]): note = "beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound)"
        f.write(f"| {r['scheme']} | {r['role']} | {r['component']} | {r['variant']} | {r['claimed']} | "
                f"{fmt(r['core292'])} | {fmt(r['core265'])} | {fmt(r['matzov'])} | {r.get('matzov_attack','')} | {note} |\n")
print(open("results/summary.md").read())
