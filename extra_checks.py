"""Additional checks: Kyber512 calibration, NTRU circulant variant for Hough et al.,
Epoque n=300 under MATZOV for large sigma, EVOLVE binding curve under 0.265 beta."""
import sys, os, json, io, contextlib
from math import log2, sqrt
sys.path.insert(0, os.environ.get("LE_PATH", "lattice-estimator"))
from estimator import LWE, SIS, NTRU, ND, RC, schemes
from estimator.reduction import ADPS16
from params import evolve_bounds, q_evolve
M = {"core292": ADPS16(mode="classical"), "core265": ADPS16(mode="quantum"), "matzov": RC.MATZOV}
def best(r):
    return min(((log2(float(v["rop"])) if float(v["rop"]) > 0 else float("inf")), k, dict((kk, str(vv)) for kk, vv in v.items())) for k, v in r.items())
def run(item):
    out = []
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if item == "kyber512":
            a = LWE.primal_usvp(schemes.Kyber512, red_cost_model=M["core292"])
            out.append({"Kyber512 primal_usvp core292": {k: str(v) for k, v in a.items()}, "log2": log2(float(a["rop"]))})
        if item == "hough_ntru_circ":
            for m in M:
                P = NTRU.Parameters(n=2048, q=2**59, Xs=ND.DiscreteGaussian(7.12), Xe=ND.DiscreteGaussian(7.12), ntru_type="circulant")
                r = NTRU.estimate(P, red_cost_model=M[m], quiet=True)
                b = best(r); out.append({"model": m, "params": repr(P), "min_log2": b[0], "attack": b[1], "detail": b[2],
                                         "all": {k: log2(float(v["rop"])) if float(v["rop"]) > 0 else None for k, v in r.items()}})
        if item == "epoque_matzov":
            for s in [4.0, 6.0, 8.0]:
                P = LWE.Parameters(n=300, q=4093, Xs=ND.UniformMod(4093), Xe=ND.DiscreteGaussian(s), m=3601)
                r = LWE.estimate(P, red_cost_model=M["matzov"], quiet=True)
                b = best(r); out.append({"sigma": s, "min_log2": b[0], "attack": b[1]})
        if item == "evolve_sis_265":
            N, d = 256, 7; q = q_evolve()
            for lb in [26, 28, 29, 29.5, 30, 30.5]:
                P = SIS.Parameters(n=N*d, q=q, length_bound=2**lb, m=N*(2*d+1), norm=2)
                r = SIS.estimate(P, red_cost_model=M["core265"], quiet=True)
                out.append({"log2_beta": lb, "min_log2": best(r)[0]})
        if item == "afgkr_sigma":
            # Abdolmaleki et al. 2026: RLWE d = 512, q = 2^32 - 99, error distribution not stated.
            # Scan a discrete Gaussian of standard deviation sigma for secret and error (2 ring samples),
            # primal uSVP only, under classical core-SVP and MATZOV; find sigma giving 128 bits.
            qA = 2**32 - 99
            for mname in ["core292", "matzov"]:
                for ls in [0, 3, 6, 9, 10, 11, 12, 12.5, 13, 13.5, 14, 15]:
                    P = LWE.Parameters(n=512, q=qA, Xs=ND.DiscreteGaussian(2**ls), Xe=ND.DiscreteGaussian(2**ls), m=1024)
                    r = LWE.primal_usvp(P, red_cost_model=M[mname])
                    out.append({"model": mname, "log2_sigma": ls, "usvp_log2": float(log2(r["rop"])), "beta": int(r["beta"])})
                    print(mname, ls, round(log2(r["rop"]), 1), r["beta"], flush=True)
    open(f"logs/extra_{item}.log", "w").write(buf.getvalue())
    json.dump(out, open(f"results/extra_{item}.json", "w"), indent=1, default=str)
    print(item, json.dumps(out, default=str)[:1500], flush=True)
if __name__ == "__main__":
    run(sys.argv[1])
