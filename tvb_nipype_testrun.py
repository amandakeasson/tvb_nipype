# test run for tvb_nipype

from tvb_interface import * 


# define inputs

model.inputs.model_name = 'Generic2dOscillator'
model.inputs.parameters = [('a',1), ('b',1)]
sc_loader.inputs.in_file = os.path.join(cwd, 'input', 'sub-01_connectivity.mat')
sc_loader.inputs.normalize = False 
integrator.inputs.integrator_name = 'HeunStochastic'
integrator.inputs.base_dt = 0.1
integrator.inputs.noise_type = 'Additive'
monitors.inputs.monitor_types = ['Bold', 'TemporalAverage']
monitors.inputs.periods = [2000.0, 10.0]
simulate.inputs.simulation_length = 10000.0


# define iterables

integrator.iterables = ("noise_val", [0.0001, 0.001, 0.01])
sc_loader.iterables = [('in_file', [os.path.join(cwd, 'input', 'sub-01_connectivity.mat'), os.path.join(cwd, 'input', 'sub-02_connectivity.mat'), os.path.join(cwd, 'input', 'sub-03_connectivity.mat')])]
simulate.iterables = [('global_coupling', np.linspace(0.5, 1.5, 3))]


# write graph

workflow.write_graph(graph2use='exec', dotfilename='./graph_testrun.dot')


# run workflow in parallel
print('running workflow...')
# workflow.run('MultiProc', plugin_args={'n_procs': 8})



