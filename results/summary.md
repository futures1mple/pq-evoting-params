| scheme | role | component | variant | claimed | 0.292b | 0.265b | MATZOV | best attack (MATZOV) | note |
|---|---|---|---|---|---|---|---|---|---|
| EVOLVE | privacy | BDLOP commitment, hiding (M-LWE) | main | 119 (time) / 93 (space), PQ | 163.0 | 148.7 | 188.3 | dual_hybrid |  |
| EVOLVE | correctness | BDLOP binding, honest openings | honest | 180 (time) / 141 (space), PQ | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| EVOLVE | correctness | BDLOP binding at B_r from Sec. 5 | sec5 | 180 (time) / 141 (space), PQ | 11.7 | 10.6 | 45.0 | large_norm | beta=2^35.3 above the linear-algebra norm (rule R4): trivial |
| EVOLVED | privacy | commitment hiding, single-candidate | single-candidate | 172.2 (primal, 0.265b) | 163.0 | 148.7 | 188.3 | dual_hybrid |  |
| EVOLVED | privacy | commitment hiding, multi-candidate k=10 | multi-candidate k=10 | 439.9 (primal, 0.265b) | 163.0 | 148.7 | 188.3 | dual_hybrid |  |
| EVOLVED | privacy | commitment hiding, instant run-off k=7 | instant run-off k=7 | 4468.2 (primal, 0.265b) | 163.0 | 148.7 | 188.3 | dual_hybrid |  |
| Epoque | privacy | ABB-type IBE, n=100 | sigma=1.0 | 'low' (no bits) | 11.7 | 10.6 | 39.9 | usvp |  |
| Epoque | privacy | ABB-type IBE, n=100 | sigma=3.2 | 'low' (no bits) | 14.3 | 13.0 | 41.2 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=200 | sigma=1.0 | 'medium' (no bits) | 29.5 | 26.8 | 56.2 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=200 | sigma=3.2 | 'medium' (no bits) | 47.3 | 42.9 | 72.4 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=300 | sigma=1.0 | 128-192 ('med-high') | 53.7 | 48.8 | 79.2 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=300 | sigma=3.2 | 128-192 ('med-high') | 80.6 | 73.1 | 103.7 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=400 | sigma=1.0 | 'higher' (no bits) | 78.6 | 71.6 | 103.1 | bdd |  |
| Epoque | privacy | ABB-type IBE, n=400 | sigma=3.2 | 'higher' (no bits) | 114.8 | 104.1 | 136.3 | bdd |  |
| Aranha et al. | privacy | BGV encryption (DKS^inf_{N,2}) | main | 168 (DKS^inf) | 146.9 | 133.6 | 174.6 | dual_hybrid |  |
| Aranha et al. | privacy | BDLOP hiding, l_c=2 (k=4) | main | 168 (DKS^inf) | 146.9 | 133.6 | 174.6 | dual_hybrid |  |
| Aranha et al. | correctness | BDLOP binding SKS^2, k=3 | k=3 | 262 (SKS^2) | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| Aranha et al. | correctness | BDLOP binding SKS^2, k=4 | k=4 | 262 (SKS^2) | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| Hough et al. | privacy | encryption randomness (RLWE, h treated as uniform) | main | 128 | 81.9 | 74.5 | 111.1 | bdd |  |
| Hough et al. | privacy | NTRU key (f,g) ~ D_7.12 | main | 128 | 44.1 | 40.0 | 76.0 | dsd |  |
| Hough et al. | privacy | BDLOP hiding | main | 128 | 81.9 | 74.5 | 111.1 | bdd |  |
| Hough et al. | correctness | BDLOP binding RSIS | main | >=128 (delta < 1.0045) | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| Farzaliyev et al. | privacy | BGV encryption (RLWE, 2 samples) | main | 192 (target); 200 classical / 182 PQ (Table 3) | 197.5 | 179.7 | 222.9 | dual_hybrid |  |
| Farzaliyev et al. | privacy | BDLOP hiding (MLWE_lambda, lambda=1) | main | 192 (target) | 197.5 | 179.7 | 222.9 | dual_hybrid |  |
| PQKryvos | privacy | BDLOP hiding (MLWE) | main | 150 (time) / 100 (space), PQ | 120.3 | 109.4 | 148.8 | dual_hybrid |  |
| PQKryvos | correctness | BDLOP binding, single opening | single | 150 / 100 | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| PQKryvos | correctness | binding of the aggregate, N_V=10^6 | aggregate N_V=10^6 | 150 / 100 | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| Boyen-Haines-Mueller | privacy | Regev-type KEM (plain LWE) | main | 240 (target) | 212.0 | 192.4 | 230.5 | bdd |  |
| Bootle et al. | privacy | MLPKE (MLWE, k=2) | main | >=128 | 243.7 | 223.0 | 264.1 | dual_hybrid |  |
| Bootle et al. | privacy | OTSE (MLWR 2^6 -> 2^4, binary secret) | main | >=128 | 172.7 | 159.3 | 192.7 | dual_hybrid |  |
| Bootle et al. | privacy | commitment hiding (MLWE_{2,2,eta}) | main | >=128 | 243.7 | 223.0 | 264.1 | dual_hybrid |  |
| Aranha et al. 2021 | privacy | verifiable encryption (MLWE, rank 2) | main | not stated separately ('much higher' than commitments) | 88.2 | 80.3 | 117.1 | bdd |  |
| Aranha et al. 2021 | privacy | BDLOP hiding (DKS^inf_{n+1,k,1}) | main | >=100 | 72.1 | 65.5 | 100.1 | bdd |  |
| Aranha et al. 2021 | correctness | BDLOP binding SKS^2_{n,k,16 sigma_C sqrt(nu N)} | main | >=100 | 118.3 | 107.3 | 145.2 | lattice |  |
| Farzaliyev et al. 2021 | privacy | RLWE encryption | main | 180 (PQ) | 193.3 | 176.0 | 219.3 | dual_hybrid |  |
| Farzaliyev et al. 2021 | privacy | BDLOP hiding (MLWE_lambda, lambda=1) | main | root Hermite factor 1.0029 | 196.5 | 178.9 | 222.3 | dual_hybrid |  |
| Farzaliyev et al. 2021 | correctness | MSIS_{mu, 8 d beta'} (l_inf) | main | 128-bit soundness; root Hermite factor 1.003 | inf | inf | inf | lattice | beyond BKZ (estimator returns inf: no block size up to the lattice dimension reaches the bound) |
| Herranz et al. 2021 | privacy | RLWE (LPR) encryption, set 1 | main | 128 | 69.2 | 62.8 | 91.9 | bdd |  |
| Herranz et al. 2021 | privacy | RLWE (LPR) encryption, set 2 | main | 128 | 80.3 | 72.9 | 105.7 | bdd |  |
| de Perthuis and Peters 2024 | privacy | FV (RLWE) layer of TREnc | main | > 140 (LWE), > 128 overall | 196.2 | 178.1 | 224.1 | dual_hybrid |  |
| Abdolmaleki et al. 2026 | privacy | RLWE encryption (shuffled ciphertexts) | main | 128 | 22.2 | 20.1 | 52.4 | bdd |  |
| Abdolmaleki et al. 2026 | privacy | ABDLOP hiding (MLWE, Ajtai shuffle argument) | main | 128 (parameters following LNP22) | 98.4 | 89.3 | 125.5 | dual_hybrid |  |
