# TVB simulations in nipype

## SETUP:
```
conda env create --name tvbenv --file tvb_environment.yml
source activate tvbenv
mkdir input
mkdir output
```
If you are using a Mac, run this command:

`echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc`


## DOCUMENTATION:

* refer to the document below for information about neural mass models (NMMs) and paramters in each model

https://github.com/the-virtual-brain/tvb-library/tree/trunk/tvb/simulator

## Instructions for running simulations:


### 1) Input files:

In the "input" directory, make files for each subject called <subjectid>_connectivity.mat.
The .mat file should contain adjacency matrices for the structural connectivity weights ("sc_weights"), the tract lengths ("tract_lengths") and the functional connectivity ("fc").

### 2) simulations script:

In the sim_run.py file, change the variables under the "THINGS TO CHANGE" heading, including:

* which model you want to run (see https://github.com/the-virtual-brain/tvb-library/tree/trunk/tvb/simulator/models for the models)

* model parameters: the script is currently set up to define global_coupling and noise in the network. You can also change the model's local parameters if you don't want to use the defaults. To do this, check the github link to see the different parameters for each model. You can add as many as you want as additional input arguments. For example, in the generic 2d oscillator model, there is a local parameter called "g". So you could add the line "mymodel.g[0] = sys.argv[4], for instance, and then the value you want to test would be added as an additional input when you run the command (see below). Most parameters have a minumum and maximum value (also specified in the github doc), so make sure the value you choose is in that range.

* pse_name: name for your parameter space explortation

* TR: the TR of your empirical bold data

* simmins: the length of your simulation in minutes (should be the same as the length of your empirical bold data)

* dtval: the integration step size ("dtval. 0.5 seems to work well for the oscillator.

### 3) run the script using the following command:

python sim_run.py <subject> <global_coupling_value> <noise_value>

if you add additional parameters:

python sim_run.py <subject> <global_coupling_value> <noise_value> <new_param_1> <new_param_2> ... <new_param_last>

### 4) output:

An output file will be saved which includes your simulation name, subject, and the values of the other input parameters, e.g. simtest1_subj01_1.0_0.001.mat

### 5) fit between simulated and empirical data

The script will also print out the correlation between the simulation and empirical FC (this correlation will also be saved in the output .mat file). It also updates you on the simulation progress (every 10s of simulated data).



## TEST RUN:

`python sim_run.py sub-01 1.0 0.001`
