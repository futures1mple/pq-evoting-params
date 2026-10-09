# Uniform re-estimation of lattice-based e-voting parameters

Scripts and full logs for re-estimating the concrete security of published
lattice-based e-voting parameter sets with a single, fixed version of the
lattice estimator.

* Estimator: <https://github.com/malb/lattice-estimator>, commit
  `53da5982597709ba0fdf94ea37a84d822310fd84` (19 Aug 2026).
  PQKryvos hiding is additionally run at the authors' commit `352ddaf` (17 Sep 2025).
* Sage: passagemath 10.8.12 (pip), Python 3.13.
* Cost models: core-SVP classical `2^(0.292 beta)`, core-SVP quantum
  `2^(0.265 beta)` (both `ADPS16`), and `MATZOV`. All attacks the estimator
  runs by default are kept in the logs; the reported value is the minimum.

## Files

| file | content |
|---|---|
| `params.py` | every problem instance, with source (page/table), translation rule and explicit assumptions |
| `run.py` | runs one instance under one cost model; writes `results/*.json`, `logs/*.log` |
| `sensitivity.py` | sensitivity to the assumptions (Epoque noise, approximate moduli, LWR model, sample count, EVOLVE SIS bound) |
| `summarize.py` | builds `results/summary.csv` and `results/summary.md` |
| `extra_checks.py` | Kyber512 calibration, circulant NTRU variant, Epoque under MATZOV, EVOLVE SIS curve under 0.265 beta |
| `make_figure.py` | draws `fig_models.pdf` (Fig. 1 of the paper) from the results |
| `jobs.txt` | list of all (instance, cost model) runs |
| `ntru_calibration.py` | NTRU estimator on the instance discussed in Hough et al., Sec. 4.2 |
| `reproduce.sh` | reproduces everything |
| `results/` | one JSON file per run (cheapest attack, cheapest primal attack, all attacks), `summary.csv`, `summary.md` |
| `logs/` | full estimator output of every run |
| `results_352ddaf/`, `logs_352ddaf/` | PQKryvos hiding at the authors' estimator commit |

## Translation rules

See `TRANSLATION` in `params.py`: module/ring problems are flattened to plain
LWE/SIS of dimension (rank x ring degree); a commitment `C r` with `C` of size
`h x w` is hiding under M-LWE with secret rank `w - h` and `h` samples; binding
is M-SIS on the top block, with the norm used by the authors. Binding is
reported as trivial when the bound exceeds the norm of solutions found by
linear algebra alone: about `q sqrt(rows/12)` in l2 (vectors `(x, -A'x)`), or
`(q-1)/2` in l_inf. The vectors `q e_i` do not count, since they open to the
same message. "Beyond BKZ" means the estimator returns infinity: no block size
up to the full lattice dimension reaches the bound.

## Reproducing

```
python -m venv venv && . venv/bin/activate && pip install passagemath-standard matplotlib
./reproduce.sh
```
A full run takes about 3 hours on two cores.

## Paper

J. Alizadeh, "How Secure Are Post-Quantum E-Voting Parameters? A Uniform
Re-Estimation of Published Lattice-Based Schemes", manuscript, 2026.

## License

MIT, see `LICENSE`.
