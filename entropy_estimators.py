import scipy.spatial as ss
import math
import numpy.random as nr
import random

##!!!Estimatore per la MI con algoritmo da Kraskov et al. 2004
def mi(x,y,k=3,base=2):
  """ Mutual information of x and y
      x,y should be a list of vectors, e.g. x = [[1.3],[3.7],[5.1],[2.4]]
      if x is a one-dimensional scalar and we have four samples
  """
  assert len(x)==len(y), "Lists should have same length"
  assert k <= len(x) - 1, "Set k smaller than num. samples - 1"
  intens =  1e-12 #small noise to break degeneracy, see doc.
  x = [list(p + intens*nr.rand(len(x[0]))) for p in x]
  y = [list(p + intens*nr.rand(len(y[0]))) for p in y]
  points = zip2(x,y)
  #Find nearest neighbors in joint space, p=inf means max-norm
  tree = ss.cKDTree(points)
  dvec = [tree.query(point,k+1,p=float('inf'))[0][k] for point in points]
  a,b,c,d = avgdigamma(x,dvec), avgdigamma(y,dvec), digamma(k), digamma(len(x))
  return (-a-b+c+d)#/log(base)
############################################################################

#####UTILITY FUNCTIONS
def vectorize(scalarlist):
  """ Turn a list of scalars into a list of one-d vectors
  """
  return [(x,) for x in scalarlist]

def shuffle_test(x,y,z=False,ns=10,ci=0.95,**kwargs):#measure,
  """ Shuffle test
      Repeatedly shuffle the x-values and then estimate measure(x,y,[z]).
      Returns the mean and conf. interval ('ci=0.95' default) over 'ns' runs.
      'measure' could me mi,cmi, e.g. Keyword arguments can be passed.
      Mutual information and CMI should have a mean near zero.
  """
  xp = x[:] #A copy that we can shuffle
  outputs = []
  for i in range(ns):
    random.shuffle(xp)
    if z:
      outputs.append(mi(xp,y,z,**kwargs))
    else:
      outputs.append(mi(xp,y,**kwargs))
  outputs.sort()


  sigma=0.0;
  med=0.0;

  for i in range (0,ns):
    med+=outputs[i]

  med*=1/ns

  for i in range (0,ns):
   sigma+=(outputs[i]-med)*(outputs[i]-med)

  sigma=math.sqrt(sigma)
  sigma*=1/(math.sqrt(ns))
  sigma*=1.96

  return med,sigma;

#####INTERNAL FUNCTIONS

def avgdigamma(points,dvec):
  #This part finds number of neighbors in some radius in the marginal space
  #returns expectation value of <psi(nx)>
  N = len(points)
  tree = ss.cKDTree(points)
  avg = 0.
  for i in range(N):
    dist = dvec[i]
    #subtlety, we don't include the boundary point,
    #but we are implicitly adding 1 to kraskov def bc center point is included
    num_points = len(tree.query_ball_point(points[i],dist-1e-15,p=float('inf')))
    avg += digamma(num_points)/N
  return avg

def zip2(*args):
  #zip2(x,y) takes the lists of vectors and makes it a list of vectors in a joint space
  #E.g. zip2([[1],[2],[3]],[[4],[5],[6]]) = [[1,4],[2,5],[3,6]]
  return [sum(sublist,[]) for sublist in zip(*args)]

