import warnings
warnings.filterwarnings('ignore')
import os, sys, scipy.io, numpy as np
from nipype import Node, Function, Workflow
#from tvb.simulator.lab import *

# https://miykael.github.io/nipype_tutorial/notebooks/basic_workflow.html

# done
def make_pse(parameter_ranges): # done, need to wrap
    import numpy as np
    pse_list = dict(parameter_ranges)
    return pse_list

# done
def make_model(model_name, parameters):# done
    import warnings
    warnings.filterwarnings('ignore')
    from tvb.simulator.lab import models
    import numpy as np
    mod = getattr(models, model_name)
    model_class = mod(**dict(parameters))
    return model_class

# done
def load_connectivity_mat(in_file, normalize=False):
     import scipy.io
     datamat = scipy.io.loadmat(in_file)
     sc_weights = datamat['sc_weights']
     if normalize:
         sc_weights = sc_weights / sc_weights.max()
     tract_lengths = datamat['tract_lengths']
     return sc_weights, tract_lengths

# done
def make_connectivity(weights, lengths):
    import warnings
    warnings.filterwarnings('ignore')
    from tvb.simulator.lab import connectivity
    conn_class = connectivity.Connectivity(weights=weights, tract_lengths=lengths)
    return conn_class

def make_integrator(integrator_name, base_dt, noise_type, noise_val):
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    from tvb.simulator.lab import integrators #, noise
    temp_integrator = getattr(integrators,integrator_name)
    #temp_noise = getattr(noise, noise_type)
    #noise = temp_noise(nsig = np.array(noise_val))
    # integrator_class = temp_integrator(dt = base_dt, noise = noise)
    integrator_class = temp_integrator(dt = base_dt)
    return integrator_class

def make_monitors(monitor_type='Raw'):
    import warnings
    warnings.filterwarnings('ignore')
    from tvb.simulator.lab import monitors
    monitor_class = getattr(monitors,monitor_type)
    return monitor_class

def run_simulation(out_file, model_input, conn_input, integrator_input, monitor_input, global_coupling = 0.1, conduction_speed=2.0, simulation_length=1000.0):
    import warnings
    warnings.filterwarnings('ignore')
    from tvb.simulator.lab import simulator
    sim = simulator.Simulator(model=model_class, connectivity=conn_class, coupling = coupling.Linear(a = global_coupling),
                             integrator = integrator_class, monitors = monitor_class,
                             simulation_length = simulation_length, conduction_speed = conduction_speed)
    sim.configure()
    (time, data), (tavg_time, tavg_data), _ = sim.run()
    np.save(out_file, data)
    return data
# https://miykael.github.io/nipype_tutorial/notebooks/basic_function_interface.html
##### NIPYPE PORTION
# done
pse_params = Node(
    Function(
        input_names=['parameter_ranges'],
        output_names=['model_class'],
        function=make_pse
    ),
    name='create_pse'
)

# done
model = Node(
    Function(
        input_names=['model_name', 'parameters'],
        output_names=['model_class'],
        function=make_model
    ),
    name='create_model'
)

# done 
sc_loader = Node(
    Function(
        input_names=['in_file', 'normalize'],
        output_names=['sc_weights', 'tract_lengths'],
        function=load_connectivity_mat
    ),
    name='load_sc_mat'
)

# done
sc = Node(
    Function(
        input_names=['weights', 'lengths'],
        output_names=['conn_class'],
        function=make_connectivity
    ),
    name='create_sc'
)

integrator = Node(
    Function(
        input_names=['integrator_name','base_dt','noise_type','noise_val'],
        output_names=['integrator_class'],
        function=make_integrator
    ),
    name='create_integrator'
)

monitors = Node(
    Function(
        input_names=['monitor_type'],
        output_names=['monitor_class'],
        function=make_monitors
    ),
    name='create_monitors'
)

simulate = Node(
    Function(
        input_names=['out_file', 'model_input', 'conn_input', 'integeator_input', 'monitor_input',
                     'global_coupling', 'conduction_speed', 'simulation_length'],
        output_names=['data'],
        function=run_simulation
    ),
    name='simulate'
)

workflow = Workflow(name='tvb_demo')
workflow.connect([
    (model, simulate, [("model_class", "model_input")]),
    (sc_loader, sc, [("sc_weights", "weights"), ("tract_lengths", "lengths")]),
    (sc, simulate, [("conn_class", "conn_input")]),
    (integrator, simulate, [("integrator_class", "integrator_input")]),
    (monitors, simulate, [("monitor_class", "monitor_input")])
])

# NOW DEFINE YOUR INPUTS
# https://miykael.github.io/nipype_tutorial/notebooks/basic_data_input.html
model.inputs.model_name = 'Generic2dOscillator'
model.inputs.parameters = [('a',1),('b',1)]
# https://miykael.github.io/nipype_tutorial/notebooks/basic_iteration.html
# workflow.model.iterables = ('parameters', [4, 8, 16])
sc_loader.inputs.in_file = '/mnt/c/Users/easso/docs/neurohackademy/tvb_nipype/input/sub-01_connectivity.mat'
sc_loader.inputs.normalize = False 
sc.inputs.lengths = 'input/'
workflow.integrator.inputs.integrator_name = 'HeunStochastic'
workflow.integrator.inputs.base_dt = 0.1
workflow.integrator.inputs.noise_type = 'Additive'
workflow.integrator.inputs.noise_val = 0.0001
#workflow.integrator.iterables = ('noise', [1, 2, 3, 4])
workflow.monitor.inputs.monitor_type = 'Raw'
#workflow.run('MultiProc', plugin_args={'n_procs': 10})

workflow.write_graph(graph2use = 'orig', dotfilename = './graph_orig/dot')

from IPython.display import Image
Image(filename="graph_orig.png")
workflow.run()