"""
Problem instances for the uniform re-estimation of published lattice-based
e-voting parameters.

Every instance is a plain LWE / NTRU / SIS problem obtained from the scheme's
ring or module problem by the translation rules in TRANSLATION below.
Each entry records the source (page/table of the paper) and every assumption
that is not stated by the authors (field `assumptions`).

Roles:
  privacy     -- hiding of commitments / IND-CPA of encryption (long-term)
  correctness -- binding of commitments / soundness (until the end of the election)
"""
from math import sqrt, comb, log2

TRANSLATION = """
R1  Ring/Module-LWE over R_q = Z_q[X]/(Phi_m), deg N, secret rank k, l samples
    -> LWE with n = k*N, m = l*N, same coefficient distributions.
R2  Commitment Com(r) = C r with C in R_q^{h x w}, C = (C1 | C2), C2 invertible
    (h x h): hiding <=> M-LWE with secret r1 in R^{w-h} and h samples
    -> LWE n = (w-h)*N, m = h*N.
R3  Binding: M-SIS on the top block A in R_q^{a x w}  -> SIS n = a*N, m = w*N,
    norm as stated by the authors (l2 or l_inf).
R4  Binding is broken by a kernel vector whose image under the message rows is
    nonzero mod q (q*e_i does not qualify). For A = (A' | I) the vectors (x, -A'x),
    x a unit vector, are found by linear algebra and have l2 norm ~ q*sqrt(rows/12).
    An instance whose bound exceeds this norm is reported as 'trivial'.
R5  Gaussian of standard deviation s -> DiscreteGaussian(s); uniform over
    {-B..B} -> Uniform(-B,B); centred binomial eta -> CenteredBinomial(eta).
"""

def q_evolve():
    return 2**31 - 2**7 - 2**5 + 1

P_GL = 2**64 - 2**32 + 1

# ---------------------------------------------------------------- EVOLVE
def evolve_bounds(n=256, d=7, sigma=1.0, NA=4, l=30):
    """Section 5 (p.13 of ePrint 2017/1235): constraints on B_r."""
    BOR = 2*NA*sqrt(n*(2*d+1))*sigma
    BpOR = 44*sqrt(60*n*(2*d+1))*BOR
    BA1 = 2*sqrt(n*(2*d+1))*sigma
    BpA1 = 2684*n*sqrt(2*d+1)*BA1
    BA2 = 2*(l+1)*sqrt(n*(2*d+1))*sigma
    BpA2 = 2684*n*sqrt(2*d+1)*BA2
    cons = {"(3) 2B'_OR": 2*BpOR, "(4) 2sqrt(60)N_A B'_Amo1": 2*sqrt(60)*NA*BpA1,
            "(7) (l+1)B'_Amo1": (l+1)*BpA1, "(8) B'_Amo2": BpA2}
    return cons, max(cons.values())

def hough_kappa(N=2048, lam=128):
    for k in range(1, 200):
        if k + log2(comb(N, k)) > lam:
            return k

PROBLEMS = []

def add(**kw):
    kw.setdefault("assumptions", [])
    kw.setdefault("variant", "main")
    PROBLEMS.append(kw)

# ---------------------------------------------------------------- EVOLVE
N, d = 256, 7
q = q_evolve()
add(id="evolve_hide", scheme="EVOLVE", role="privacy", component="BDLOP commitment, hiding (M-LWE)",
    kind="LWE", n=N*d, m=N*(d+1), q=q, Xs=("DG", 1.0), Xe=("DG", 1.0),
    claimed="119 (time) / 93 (space), PQ", tool="[APS15] + NewHope analysis",
    source="Table 2 and Sec. 5, p.13; Sec. 3.1, p.8",
    assumptions=["translation R2: C in R^{(d+1)x(2d+1)}, secret rank d, d+1 samples"])
cons, Br = evolve_bounds()
add(id="evolve_bind_honest", scheme="EVOLVE", role="correctness", component="BDLOP binding, honest openings",
    kind="SIS", n=N*d, m=N*(2*d+1), q=q, beta=2*2*sqrt(N*(2*d+1))*1.0, norm=2,
    claimed="180 (time) / 141 (space), PQ", tool="[APS15] + NewHope analysis",
    source="Sec. 3.1 p.8, Table 2 p.13",
    variant="honest", assumptions=["bound 2*||r||, ||r|| <= 2 sigma sqrt(N(2d+1)) (tail bound); lower bound on the relevant norm"])
add(id="evolve_bind_sec5", scheme="EVOLVE", role="correctness", component="BDLOP binding at B_r from Sec. 5",
    kind="SIS", n=N*d, m=N*(2*d+1), q=q, beta=2*Br, norm=2,
    claimed="180 (time) / 141 (space), PQ", tool="[APS15] + NewHope analysis",
    source="Sec. 5 constraints (3),(4),(7),(8), p.13",
    variant="sec5", assumptions=["B_r = max of the four consistency constraints with Table 2 values; SIS bound 2B_r"])

# ---------------------------------------------------------------- EVOLVED
# commitment key (d+k) x (2d+k); hiding secret rank d, d+k samples
for k, label in [(1, "single-candidate"), (10, "multi-candidate k=10"), (120, "instant run-off k=7")]:
    add(id=f"evolved_hide_k{k}", scheme="EVOLVED", role="privacy", component=f"commitment hiding, {label}",
        kind="LWE", n=N*d, m=N*(d+k), q=q, Xs=("DG", 1.0), Xe=("DG", 1.0),
        claimed={1: "172.2 (primal, 0.265b)", 10: "439.9 (primal, 0.265b)", 120: "4468.2 (primal, 0.265b)"}[k],
        tool="estimator [APS15], version not stated; LWE dim 256*(7+m)",
        source="Sec. 8.2, p.12-13, Fig. 8",
        variant=label,
        assumptions=["translation R2 with key (d+k)x(2d+k) (Sec. 3, p.5): secret rank d=7, d+k samples",
                     "k = message slots (k=120 for IRV with 7 candidates gives LWE dim 256*127 as in Fig. 8)"])

# ---------------------------------------------------------------- Epoque
for (n_, m2) in [(100, 2400), (200, 4800), (300, 7200), (400, 9600)]:
    for s in [1.0, 3.2]:
        add(id=f"epoque_ibe_n{n_}_s{s}", scheme="Epoque", role="privacy",
            component=f"ABB-type IBE, n={n_}", kind="LWE", n=n_, m=m2//2 + 1, q=4093,
            Xs=("U", None), Xe=("DG", s),
            claimed={100: "'low' (no bits)", 200: "'medium' (no bits)", 300: "128-192 ('med-high')",
                     400: "'higher' (no bits)"}[n_],
            tool="not stated", source="Table 2, p.11; Sec. 5.1, p.8",
            variant=f"sigma={s}",
            assumptions=["noise distribution not given; sigma is an assumption (sensitivity: 1.0 and 3.2)",
                         "uniform secret s in Z_q^n; m+1 samples (y and c0); R^T y part not counted"])

# ---------------------------------------------------------------- Aranha et al.
Nq = 4096
add(id="abgs_bgv", scheme="Aranha et al.", role="privacy", component="BGV encryption (DKS^inf_{N,2})",
    kind="LWE", n=Nq, m=2*Nq, q=2**78, Xs=("T", None), Xe=("T", None),
    claimed="168 (DKS^inf)", tool="LWE-estimator (version not stated)",
    source="Table 5 p.23; Thm 1 p.4",
    assumptions=["q = 2^78 for 'q ~ 2^78'", "ternary uniform secret and noise (B_Key = B_Err = 1)"])
add(id="abgs_com_hide", scheme="Aranha et al.", role="privacy", component="BDLOP hiding, l_c=2 (k=4)",
    kind="LWE", n=Nq*1, m=Nq*3, q=2**78, Xs=("T", None), Xe=("T", None),
    claimed="168 (DKS^inf)", tool="LWE-estimator", source="Thm 3 p.5; Table 5 p.23",
    assumptions=["k = l_c + 2 with l_c = 2: secret rank k-(n+l_c) = 1"])
beta_abgs = 16 * 2**12 * sqrt(36*Nq)
for k in [3, 4]:
    add(id=f"abgs_com_bind_k{k}", scheme="Aranha et al.", role="correctness", component=f"BDLOP binding SKS^2, k={k}",
        kind="SIS", n=Nq*1, m=Nq*k, q=2**78, beta=beta_abgs, norm=2,
        claimed="262 (SKS^2)", tool="root Hermite factor 1.00225", source="Thm 3 p.5; Table 5 p.23",
        variant=f"k={k}",
        assumptions=["beta = 16 sigma_C sqrt(nu N) with sigma_C = 2^12 (Table 5 gives '~2^12')"])

# ---------------------------------------------------------------- Hough et al.
Nh = 2048
add(id="hough_rlwe", scheme="Hough et al.", role="privacy", component="encryption randomness (RLWE, h treated as uniform)",
    kind="LWE", n=Nh, m=Nh, q=2**59, Xs=("T", None), Xe=("T", None),
    claimed="128", tool="estimator [APS15], cost 0.292b+16.4+log(8d)", source="Table 2 and p.29; Fig. 2 p.9",
    assumptions=["q = 2^59 for 'q ~ 2^59'", "s,e uniform in S_1 (ternary)"])
add(id="hough_ntru", scheme="Hough et al.", role="privacy", component="NTRU key (f,g) ~ D_7.12",
    kind="NTRU", n=Nh, q=2**59, Xs=("DG", 7.12), Xe=("DG", 7.12),
    claimed="128", tool="DvW21 fatigue analysis, 0.292b+16.4+log2(8d)", source="Table 2 p.29; Sec. 4",
    assumptions=["q = 2^59"])
kap = hough_kappa()
sigCom = kap * 1 * sqrt(3*Nh)
add(id="hough_com_hide", scheme="Hough et al.", role="privacy", component="BDLOP hiding",
    kind="LWE", n=Nh, m=2*Nh, q=2**59, Xs=("T", None), Xe=("T", None),
    claimed="128", tool="estimator [APS15]", source="Lemma 3 p.11",
    assumptions=["k = 3 (matrix on p.11), 2 rows: secret 1 ring element, 2 samples"])
add(id="hough_com_bind", scheme="Hough et al.", role="correctness", component="BDLOP binding RSIS",
    kind="SIS", n=Nh, m=3*Nh, q=2**59, beta=16*sigCom*sqrt(kap*Nh), norm=2,
    claimed=">=128 (delta < 1.0045)", tool="MR09 root Hermite factor", source="Lemma 3 p.11; p.30; Table 6 p.42",
    assumptions=[f"kappa = {kap} (smallest with 2^k*C(d,k) > 2^128, Table 6)", "k = 3, sigma_Com = kappa*B_Com*sqrt(k d)"])

# ---------------------------------------------------------------- Farzaliyev et al.
Nf = 4096
add(id="farz_bgv", scheme="Farzaliyev et al.", role="privacy", component="BGV encryption (RLWE, 2 samples)",
    kind="LWE", n=Nf, m=2*Nf, q=2**62, Xs=("T", None), Xe=("T", None),
    claimed="192 (target); 200 classical / 182 PQ (Table 3)", tool="LWE Estimator [APS15], version not stated",
    source="p.23; Sec. 3.6.3 p.8; Table 3 p.28",
    assumptions=["q = 2^62 for 'q ~ 2^62'", "uniform ternary (Pr = 1/3)"])
add(id="farz_com_hide", scheme="Farzaliyev et al.", role="privacy", component="BDLOP hiding (MLWE_lambda, lambda=1)",
    kind="LWE", n=Nf, m=4*Nf, q=2**62, Xs=("T", None), Xe=("T", None),
    claimed="192 (target)", tool="LWE Estimator [APS15]", source="Sec. 3.6.2 p.8; p.23",
    assumptions=["mu + l = 4 samples (l = 3 messages, representative)"])

# ---------------------------------------------------------------- PQKryvos
Nk, dk = 486, 6
add(id="pqk_hide", scheme="PQKryvos", role="privacy", component="BDLOP hiding (MLWE)",
    kind="LWE", n=Nk*dk, m=Nk*(dk+1), q=P_GL, Xs=("T", None), Xe=("T", None),
    claimed="150 (time) / 100 (space), PQ", tool="lattice-estimator 352ddaf (Sep 17, 2025)",
    source="p.1158, p.1159, ref. [71]; Thm 2 p.1156",
    assumptions=["translation R2 (A in R^{(d+1)x(2d+1)}), ring Z[X]/Phi_729 of degree 486 treated as degree-486 module ring",
                 "beta = 1: uniform ternary"])
mk = Nk*(2*dk+1)
add(id="pqk_bind_single", scheme="PQKryvos", role="correctness", component="BDLOP binding, single opening",
    kind="SIS", n=Nk*dk, m=mk, q=P_GL, beta=2*sqrt(mk), norm=2,
    claimed="150 / 100", tool="lattice-estimator 352ddaf", source="Thm 2 p.1156",
    variant="single", assumptions=["exact openings proven with ||r||_inf <= 1 (Ligero); difference has l_inf <= 2, "
                                   "converted to l2 <= 2 sqrt(m) (the l_inf SIS routine overflows for bound 2)"])
NV = 10**6
add(id="pqk_bind_agg", scheme="PQKryvos", role="correctness", component=f"binding of the aggregate, N_V=10^6",
    kind="SIS", n=Nk*dk, m=mk, q=P_GL, beta=2*NV*sqrt(mk), norm=2,
    claimed="150 / 100", tool="lattice-estimator 352ddaf", source="Thm 2; Sec. 4.3",
    variant="aggregate N_V=10^6", assumptions=["aggregate randomness l_inf <= N_V; difference l2 <= 2 N_V sqrt(m) (worst case)"])

# ---------------------------------------------------------------- Boyen-Haines-Mueller 2020
add(id="bhm_lwe", scheme="Boyen-Haines-Mueller", role="privacy", component="Regev-type KEM (plain LWE)",
    kind="LWE", n=1024, m=1024 + 8, q=2**16, Xs=("DG", 2.0), Xe=("DG", 2.0),
    claimed="240 (target)", tool="'estimates from multiple sources', FrodoKEM recommendations",
    source="Sec. 7.2 p.14; App. A p.22-23",
    assumptions=["secret from the noise distribution and m = n + 8 samples, as in FrodoKEM"])

# ---------------------------------------------------------------- Bootle et al.
Nb = 512
add(id="blm_mlwe", scheme="Bootle et al.", role="privacy", component="MLPKE (MLWE, k=2)",
    kind="LWE", n=2*Nb, m=2*Nb, q=3109, Xs=("CB", 2), Xe=("CB", 2),
    claimed=">=128", tool="not stated", source="Fig. 3 p.28; Def. 1 p.9",
    assumptions=["public key A in R^{2x2}: 2 samples"])
add(id="blm_mlwr", scheme="Bootle et al.", role="privacy", component="OTSE (MLWR 2^6 -> 2^4, binary secret)",
    kind="LWE", n=1*Nb, m=3*Nb, q=64, Xs=("B", None), Xe=("U", (-2, 1)),
    claimed=">=128", tool="not stated", source="Fig. 2 p.16; Thm 2 p.19; Fig. 3 p.28",
    assumptions=["LWR -> LWE with deterministic rounding error modelled as uniform on {-2,...,1}",
                 "k_LWE + L = 3 samples (L = 1)"])
add(id="blm_com_hide", scheme="Bootle et al.", role="privacy", component="commitment hiding (MLWE_{2,2,eta})",
    kind="LWE", n=2*Nb, m=2*Nb, q=3109, Xs=("CB", 2), Xe=("CB", 2),
    claimed=">=128", tool="not stated", source="App. B, p.40; Fig. 3",
    assumptions=["same instance shape as MLPKE"])

# ---------------------------------------------------------------- Aranha, Baum, Gjosteen, Silde, Tunge (CT-RSA 2021)
Na = 1024
add(id="abgst21_enc", scheme="Aranha et al. 2021", role="privacy", component="verifiable encryption (MLWE, rank 2)",
    kind="LWE", n=2*Na, m=3*Na, q=2**56, Xs=("T", None), Xe=("T", None),
    claimed="not stated separately ('much higher' than commitments)", tool="LWE-estimator [APS15]",
    source="Sec. 5.1 and Alg. p.20; Table 2 p.26 (ePrint 2021/338)",
    assumptions=["q = 2^56 for 'q ~ 2^56'", "l = 2: secret rank 2, l+1 = 3 samples per ciphertext block; D_1 uniform ternary"])
add(id="abgst21_com_hide", scheme="Aranha et al. 2021", role="privacy", component="BDLOP hiding (DKS^inf_{n+1,k,1})",
    kind="LWE", n=Na, m=2*Na, q=2**32, Xs=("T", None), Xe=("T", None),
    claimed=">=100", tool="LWE-estimator [APS15]", source="Sec. 3.1 p.9; Table 2 p.26; p.25",
    assumptions=["p = 2^32 for 'p ~ 2^32'", "k = 3, n = 1: secret rank k-(n+1) = 1, n+1 = 2 samples"])
add(id="abgst21_com_bind", scheme="Aranha et al. 2021", role="correctness", component="BDLOP binding SKS^2_{n,k,16 sigma_C sqrt(nu N)}",
    kind="SIS", n=Na, m=3*Na, q=2**32, beta=16*54000*sqrt(36*Na), norm=2,
    claimed=">=100", tool="LWE-estimator [APS15]", source="Sec. 3.1 p.9; Table 2 p.26",
    assumptions=["sigma_C = 54000 ('~54000'), nu = 36, N = 1024"])

# ---------------------------------------------------------------- Farzaliyev, Willemson, Kaasik (ICISC 2021; ePrint 2021/1499)
Nw = 4096
add(id="fwk21_rlwe", scheme="Farzaliyev et al. 2021", role="privacy", component="RLWE encryption",
    kind="LWE", n=Nw, m=2*Nw, q=2**63, Xs=("T", None), Xe=("T", None),
    claimed="180 (PQ)", tool="pq-crystals security-estimates script",
    source="Sec. 2.2 p.3; Sec. 4.2 p.11 (ePrint 2021/1499)",
    assumptions=["q = 2^63 for 'q ~ 2^63'", "chi_1 uniform ternary; ciphertext (u,v): 2 samples with secret r"])
add(id="fwk21_com_hide", scheme="Farzaliyev et al. 2021", role="privacy", component="BDLOP hiding (MLWE_lambda, lambda=1)",
    kind="LWE", n=Nw, m=2*Nw, q=2**63, Xs=("CB", 2), Xe=("CB", 2),
    claimed="root Hermite factor 1.0029", tool="pq-crystals security-estimates script",
    source="Sec. 2.6 p.5; Sec. 4.2 p.11-12",
    assumptions=["chi_2 with Pr[0] = 6/16 read as centred binomial eta = 2", "mu = lambda = 1: secret rank 1, mu+1 = 2 samples"])
add(id="fwk21_com_bind", scheme="Farzaliyev et al. 2021", role="correctness", component="MSIS_{mu, 8 d beta'} (l_inf)",
    kind="SIS", n=Nw, m=16*Nw, q=2**63, beta=8*Nw*2**45, norm="oo",
    claimed="128-bit soundness; root Hermite factor 1.003", tool="pq-crystals security-estimates script",
    source="Thm 1 p.7; Sec. 4.2 p.11",
    assumptions=["delta_1 = delta_2 = 2^45 (text '245'), beta' ~ 2^45, bound 8 d beta' = 2^60 in l_inf",
                 "m = 16 ring columns given to the attacker (the matrix has many more; the estimator chooses the sub-dimension)"])

# ---------------------------------------------------------------- Herranz, Martinez, Sanchez (ePrint 2021/488)
add(id="hms21_n128", scheme="Herranz et al. 2021", role="privacy", component="RLWE (LPR) encryption, set 1",
    kind="LWE", n=128, m=256, q=4099, Xs=("DG", 27.0), Xe=("DG", 27.0),
    claimed="128", tool="not stated", source="Def. 4 p.5; Sec. 5 p.13 (ePrint 2021/488)",
    assumptions=["sigma = 27 read as standard deviation; truncation at k*sigma (k = 14) ignored",
                 "s, e, r, e1, e2 from the error distribution; 2 ring samples"])
add(id="hms21_n512", scheme="Herranz et al. 2021", role="privacy", component="RLWE (LPR) encryption, set 2",
    kind="LWE", n=512, m=1024, q=1048583, Xs=("DG", 6.0), Xe=("DG", 6.0),
    claimed="128", tool="not stated", source="Def. 4 p.5; Sec. 5 p.13 (ePrint 2021/488)",
    assumptions=["sigma = 6 read as standard deviation; truncation ignored", "2 ring samples"])

# ---------------------------------------------------------------- de Perthuis, Peters (ePrint 2024/2087)
add(id="dpp24_fv", scheme="de Perthuis and Peters 2024", role="privacy", component="FV (RLWE) layer of TREnc",
    kind="LWE", n=2**14, m=2**15, q=2**255, Xs=("B", None), Xe=("B", None),
    claimed="> 140 (LWE), > 128 overall", tool="LWE estimator [APS15]",
    source="Sec. 6 p.26 (ePrint 2024/2087)",
    assumptions=["p = 2^255 for 'p on 255 bits'", "binary secret and error read as uniform on {0,1}", "2 ring samples"])

# ---------------------------------------------------------------- Abdolmaleki, Fauzi, Gu, Krips, Roustaeifar (ePrint 2026/1540)
qA = 2**32 - 99
add(id="afgkr26_rlwe", scheme="Abdolmaleki et al. 2026", role="privacy", component="RLWE encryption (shuffled ciphertexts)",
    kind="LWE", n=512, m=1024, q=qA, Xs=("T", None), Xe=("T", None),
    claimed="128", tool="lattice estimator (commit not stated)",
    source="Sec. 6.1 p.17; Sec. 6.3 p.18; Table 2 p.21 (ePrint 2026/1540)",
    assumptions=["q = 2^32 - 99 as in Table 2 (text: q ~ 2^32), d = 512", "chi not specified: uniform ternary assumed", "2 ring samples"])
add(id="afgkr26_com_hide", scheme="Abdolmaleki et al. 2026", role="privacy", component="ABDLOP hiding (MLWE, Ajtai shuffle argument)",
    kind="LWE", n=128*(25-9-5-1), m=128*(9+5+1), q=qA, Xs=("T", None), Xe=("T", None),
    claimed="128 (parameters following LNP22)", tool="lattice estimator (commit not stated)",
    source="Thm 2; Table 2 p.21 (ePrint 2026/1540)",
    assumptions=["MLWE_{n+l+1, m2-n-l-1} with n = 9, l = 5, m2 = 25, d = 128", "s2 uniform ternary (nu = 1, as in LNP22)"])
