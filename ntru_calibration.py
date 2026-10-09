import sys; sys.path.insert(0,'lattice-estimator')
from estimator import *
from estimator.reduction import ADPS16
from math import log2
for (n,lq,sig) in [(2048,66,None),(2048,74,13),(2048,59,7.12)]:
    Xs = ND.Uniform(-1,1) if sig is None else ND.DiscreteGaussian(sig)
    P = NTRU.Parameters(n=n,q=2**lq,Xs=Xs,Xe=Xs)
    print(P)
    a=NTRU.primal_usvp(P, red_cost_model=ADPS16()); print(' usvp', a)
    b=NTRU.primal_dsd(P, red_cost_model=ADPS16()); print(' dsd', b)
