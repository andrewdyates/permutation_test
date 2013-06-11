#!/usr/bin/python
"""Random selection permutation testing.

python script_single.py fname=nice.may3.Eg.expr.alltrans.celegans.csv n=1000 dep=dcor
python script_single.py fname=nice.may3.Eg.expr.alltrans.celegans.csv n=1000 dep=pcc
python script_single.py fname=nice.may3.Eg.expr.alltrans.celegans.csv n=1000 dep=pcc do_abs=T
"""
from __future__ import division
import matrix_io as mio
import numpy as np
#import multiprocessing (causes exception due to function pickling error)
import sys
import random
random.seed()

def f_dep(M, f):
  m,n = M.shape
  while True:
    a = random.randint(0,m-1)
    b = random.randint(0,m-1)
    if a != b: break
  return f(M[a,],random.sample(M[b,],k=n))

def main(fname=None, n=100000, dep="dcor", do_abs=False):
  assert fname
  n = int(n)
  if isinstance(do_abs, basestring): 
    do_abs = not do_abs.lower() in ('f','false','none')
  D = mio.load(fname)
  M = D['M']
  #POOL = multiprocessing.Pool()
  if dep=="dcor":
    import dcor
    d = dcor.dcor
    f = lambda x: f_dep(M,d)
    hist_bins = 20
    hist_range = (0,1)
  elif dep=="pcc":
    import scipy.stats
    d = lambda a,b: scipy.stats.pearsonr(a,b)[0]
    f = lambda x: f_dep(M,d)
    if do_abs:
      hist_bins = 20
      hist_range = (0,1)
    else:
      hist_bins = 40
      hist_range = (-1,1)
  else:
    raise Exception, "Unrecognized dependency measure '%s'" % dep
  #Z = np.array(POOL.map(f, xrange(n))) 
  Z = np.array(map(f, xrange(n)))
  if do_abs:
    Z = np.abs(Z)
  Z.sort()
  i = 1
  print "n=%d" % n
  print
  while i<=n:
    print i, i/n, Z[-i]
    i *= 10
  print
  print np.histogram(Z, range=hist_range, bins=hist_bins)
  
  

if __name__ == '__main__':
  args = dict((s.split('=') for s in sys.argv[1:]))
  print args
  main(**args)
