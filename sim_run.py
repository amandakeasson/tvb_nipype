#!/bin/bash

# import stuff
import os, sys, scipy.io, numpy as np
from tvb.simulator.lab import *

######################### THINGS TO CHANGE ##############################
# define model: 
mymodel = models.Generic2dOscillator()

# define model parameters:
subj = sys.argv[1]
global_coupling = float(sys.argv[2])
noise_val = float(sys.argv[3])

# define directories and filenames
simfn = 'simtest1'
simdir = '/mnt/c/Users/easso/docs/neurohackademy/tvb_test/'

# define timing
TR=2000.0                       # TR of fMRI
simmins=0.5                     # length of simulation in minutes
dtval=0.5                       # integration step size; results in NaNs if too large
##########################################################################

indir = os.path.join(simdir,'input/')
outdir = os.path.join(simdir,'output/')
results_fn = outdir + '/' + simfn + '_' + subj
for a in range(len(sys.argv)-2):
	results_fn = results_fn + '_' + sys.argv[a+2]

results_fn = results_fn + '.mat'

datamat = scipy.io.loadmat(indir + '/' + subj + '_connectivity.mat')
sc_weights = datamat['sc_weights']
sc_weights = sc_weights / sc_weights.max()
tract_lengths = datamat['tract_lengths']
emp_fc = datamat['fc']
wm = connectivity.Connectivity(weights=sc_weights, tract_lengths=tract_lengths)
wm_coupling = coupling.Linear(a = global_coupling)

##### run simulation

sim = simulator.Simulator(model=mymodel, connectivity=wm, coupling=wm_coupling, conduction_speed=3.0, 
		integrator=integrators.HeunStochastic(dt=dtval, noise=noise.Additive(nsig=np.array([noise_val]))),  
		monitors=(monitors.Bold(period=TR), monitors.TemporalAverage(period=10.0), monitors.ProgressLogger(period=10000.0)), 
		simulation_length=(simmins+1.0)*60.0*1000.0)

sim.configure()
(time, data), (tavg_time, tavg_data), _ = sim.run() # data = time x state_variables x nodes x modes

##### remove transient
data_all = data
data = data[-int(simmins*60*1000/TR):,0,:,0]
tavg_all = tavg_data
tavg_data = tavg_data[-int(simmins*60*1000/10.0):,0,:,0] # 
data = np.squeeze(data)

##### calculate sim-emp correlations
sim_fc = np.corrcoef(data.T)

for i in range(sim_fc.shape[0]):
        sim_fc[i:,i]=np.inf

for i in range(emp_fc.shape[0]):
        emp_fc[i:,i]=np.inf

sim_fc = sim_fc[~np.isinf(sim_fc)]
emp_fc = emp_fc[~np.isinf(emp_fc)]

def fisherz(rmat):
        z = 0.5*np.log((1+rmat)/(1-rmat))
        return z

sim_fc = fisherz(sim_fc)
emp_fc = fisherz(emp_fc)

sim_emp_corr = np.corrcoef(sim_fc.ravel(), emp_fc.ravel())[1, 0]

##### calculate global variance 
gvar_bold = np.var(data,axis=0); gvar_bold = np.mean(gvar_bold)

print('Sim-Emp FC Correlation = %0.4f' % sim_emp_corr) 

##### SAVE MAT FILE
scipy.io.savemat(results_fn, {'tavg_all': tavg_all, 'tavg_data': tavg_data, 'bold_data': data, 'bold_data_all': data_all, 'sim_fc': sim_fc, 'gvar_bold': gvar_bold, 'sim_emp_corr': sim_emp_corr})

