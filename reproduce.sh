#!/bin/sh
# Reproduce all results. Requires Python 3.11+ and passagemath (pip install passagemath-standard).
set -e
[ -d lattice-estimator ] || git clone https://github.com/malb/lattice-estimator.git
git -C lattice-estimator checkout 53da5982597709ba0fdf94ea37a84d822310fd84
# main runs: every instance x cost model (2 in parallel)
cat jobs.txt | xargs -P 2 -L 1 sh -c 'python run.py $0 $1'
# sensitivity analyses
for it in evolve_sis epoque_sigma q_pm1 mlwr_gauss bhm_m; do python sensitivity.py $it > logs/sens_$it.log; done
# PQKryvos hiding at the authors' estimator commit
[ -d le_352ddaf ] || git clone https://github.com/malb/lattice-estimator.git le_352ddaf
git -C le_352ddaf checkout 352ddaf4a288a0543f5d9eb588d2f89c7acec463
for m in core292 core265 matzov; do OUT_DIR=results_352ddaf LOG_DIR=logs_352ddaf LE_PATH=le_352ddaf python run.py pqk_hide $m; done
# calibration and additional checks
for it in kyber512 hough_ntru_circ epoque_matzov evolve_sis_265; do python extra_checks.py $it; done
python ntru_calibration.py > logs/ntru_calibration.log
python summarize.py
python make_figure.py
