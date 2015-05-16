"""
This PYTHON script implements a ABC MCMC algorithim to approximate the 
posterior of the succession problem of Bayes and Laplace using a uniform prior 
and a truncated normal normal for the proposal density.

This follows the algorith in 'ABC for dynamical systems' T. Toni et al 2008
"""

import numpy as np 
import scipy.stats as ss 
import matplotlib.pyplot as plt 


def q_sample(theta):
	"""return a sample from the truncated normal centered about theta
						FINISHED!!!
	"""
	r = 2
	while r >= 1 or r <= 0:
		r = np.random.normal(loc=theta, scale=0.1) 	# scale = 0.1
	return r

def q(theta_prop,theta_current):
	"""returns the value of the proposal density at theta_prop conditioned on 
	the current postion theta_current
						FINISHED!!!
	"""
	n = ss.norm(loc=theta_current, scale=0.1) 	# scale = 0.1 as in q_sample
	numerator = n.pdf(theta_prop)
	denominator = n.cdf(1) - n.cdf(0)
	return numerator/denominator

def f(theta, num_flips):
	"""returns a data set generated with the parameter theta
						FINISHED!!!
	"""
	result = np.random.binomial(n=num_flips, p=theta)
	return result

def d(X_true,X_star):
	"""returns the distance between samples via a metric on a summary statistic
						FINISHED!!!
	"""
	return abs(X_true - X_star) 

def prior(theta):
	"""returns the value of the prior distribution evaluated at theta
						FINISHED!!!
	"""
	if theta <=1 and theta >= 0:
		y = 1
	else:
		y = 0
	return y

def true_posterior(mesh, X_true, num_flips):
	"""returns the value of the true posterior evaluated on the mesh
						FINISHED!!!
	"""
	a = X_true + 1
	b = num_flips - X_true + 1
	result = ss.beta.pdf(mesh,a,b)
	return result


def ABC_MCMC(epsilon, N, X_true, num_flips):
	"""Carries out a MCMC of N steps and returns the states visited
						FINISHED!!!
	"""
	#-------------------------- M1 --------------------------#
	i = 0
	theta = 0.5
	theta_chain = [theta]
	#-------------------------- M2 --------------------------#
	while i < N:
		theta_star = q_sample(theta)
		#---------------------- M3 --------------------------#
		X_star = f(theta_star, num_flips)
		#---------------------- M4 --------------------------#
		if d(X_true,X_star) <= epsilon:
			#------------------ M5 --------------------------#
			foo = ( prior(theta_star)*q(theta,theta_star) )/( prior(theta)*q(theta_star,theta) )
			alpha = min(1, foo)
			r = np.random.uniform()
			if r <= alpha:
				theta = theta_star
		theta_chain += [theta]
		#---------------------- M6 --------------------------#
		i += 1
	return theta_chain

def main():
	epsilon = 1			# tolerance
	N = 10**5			# number of states to sample from chain
	X_true = 5			# observed number of heads
	num_flips = 10		# number of coin flips

	chain = ABC_MCMC(epsilon, N, X_true, num_flips)

	xx = np.linspace(0,1,100)
	yy = true_posterior(xx,X_true,num_flips)
	plt.plot(xx,yy,'r--')

	plt.hist(chain, bins=20, normed=True)
	plt.title("Chain Histogram")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.show()

	return None

if __name__ == '__main__':
	main()
