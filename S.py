import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats as ss 

def ABC_SMC():
	"""carries out an ABC SMC with N samples at each tolerance
						IN PROGRESS
	"""
	# S1
	t = 0
	# S2.0
	i = 1
	# S2.1
	dataset_found = False
	while not dataset_found:
		th_ss_found = False
		while not th_ss_found:
			if t == 0:
				th_ss = prior_sample() 	# sample from prior distribution
			else:
				th_s = sample_randm(m) 	# sample from previous random measure
				th_ss = perturb(th_s) 	# perturb this parameter 
			if prior_eval(th_ss) > 0: 	# check if consistent
				th_ss_found = True
		X_data = dataset_sample(th_ss)
		if d(X_data,X_true) < eps[t]:
			dataset_found = True
	# S2.2




