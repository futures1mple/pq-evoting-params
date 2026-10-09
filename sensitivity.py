"""
Sensitivity of the re-estimates to the assumptions recorded in params.py.
Cost model: core-SVP classical (0.292 beta), all LWE attacks; min over attacks.
usage: python sensitivity.py <item>   (item in epoque_sigma, q_pm1, mlwr_gauss, bhm_m, evolve_sis)
Writes results/sens_<item>.json and logs/sens_<item>.log
"""
import sys, os, json, io, contextlib
from math import log2, sqrt
sys.path.insert(0, os.environ.get("LE_PATH", "lattice-estimator"))
from estimator import LWE, SIS, ND
from estimator.reduction import ADPS16
from params import evolve_bounds, q_evolve

CM = ADPS16(mode="classical")

def lwe_min(n, q, Xs, Xe, m):
    P = LWE.Parameters(n=n, q=q, Xs=Xs, Xe=Xe, m=m)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = LWE.estimate(P, red_cost_model=CM, jobs=1, quiet=True)
    best = min((log2(float(v["rop"])), k) for k, v in r.items() if float(v["rop"]) > 0)
    return {"params": repr(P), "min_rop_log2": best[0], "attack": best[1],
            "all": {k: log2(float(v["rop"])) for k, v in r.items() if float(v["rop"]) > 0}}

def item_epoque_sigma():
    out = []
    for n_, m in [(300, 3601), (400, 4801)]:
        for s in [0.5, 1.0, 2.0, 3.2, 4.0, 6.0, 8.0]:
            r = lwe_min(n_, 4093, ND.UniformMod(4093), ND.DiscreteGaussian(s), m)
            out.append({"n": n_, "sigma": s, **r}); print(n_, s, r["min_rop_log2"], r["attack"], flush=True)
    return out

def item_q_pm1():
    out = []
    T = ND.Uniform(-1, 1)
    for name, n, m, lq in [("abgs_bgv", 4096, 8192, 78), ("hough_rlwe", 2048, 2048, 59), ("farz_bgv", 4096, 8192, 62)]:
        for d in (-1, +1):
            r = lwe_min(n, 2**(lq + d), T, T, m)
            out.append({"name": name, "log2q": lq + d, **r}); print(name, lq + d, r["min_rop_log2"], flush=True)
    return out

def item_mlwr_gauss():
    # LWR 2^6 -> 2^4: rounding error modelled as Gaussian with the same variance as Uniform{-2..1}
    s = sqrt(((4**2) - 1) / 12)
    r = lwe_min(512, 64, ND.Uniform(0, 1), ND.DiscreteGaussian(s), 1536)
    print("mlwr gaussian", s, r["min_rop_log2"]); return [{"sigma": s, **r}]

def item_bhm_m():
    out = []
    for m in [2048, 4096]:
        r = lwe_min(1024, 2**16, ND.DiscreteGaussian(2.0), ND.DiscreteGaussian(2.0), m)
        out.append({"m": m, **r}); print("bhm m", m, r["min_rop_log2"], flush=True)
    return out

def item_evolve_sis():
    """Bits of the EVOLVE binding SIS instance as a function of the bound;
    where it crosses q, and which bound would match the claimed 180 bits."""
    N, d = 256, 7
    q = q_evolve()
    cons, Br = evolve_bounds()
    out = {"constraints_log2": {k: log2(v) for k, v in cons.items()}, "Br_log2": log2(Br),
           "two_Br_log2": log2(2*Br), "q_log2": log2(q), "q_mod_32": q % 32,
           "linear_algebra_norm_log2": log2(q*sqrt(N*d/12)), "curve": []}
    for lb in [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 31, 32, 34, 35.25]:
        P = SIS.Parameters(n=N*d, q=q, length_bound=2**lb, m=N*(2*d+1), norm=2)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SIS.estimate(P, red_cost_model=CM, jobs=1, quiet=True)
        best = min(log2(float(v["rop"])) if float(v["rop"]) > 0 else float("inf") for v in r.values())
        out["curve"].append({"log2_beta": lb, "min_rop_log2": best}); print("sis", lb, best, flush=True)
    return out

if __name__ == "__main__":
    it = sys.argv[1]
    res = globals()["item_" + it]()
    os.makedirs("results", exist_ok=True)
    json.dump(res, open(f"results/sens_{it}.json", "w"), indent=1, default=str)
