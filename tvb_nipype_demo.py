import os, sys, scipy.io, numpy as np
from nipype import Node, Function, Workflow
#from tvb.simulator.lab import *
import warnings
warnings.filterwarnings('ignore')


# https://miykael.github.io/nipype_tutorial/notebooks/basic_workflow.html
def make_model(model_name, parameters):
    from tvb.simulator.lab import models, simulator
    mod = getattr(simulator.models, model_name)
    model_class = mod(**dict(parameters))
    return model_class


def make_connectivity(weights, lengths):
    from tvb.simulator.lab import connectivity, simulator
    conn_class = simulator.connectivity.Connectivity(weights, lengths)
    return conn_class


def make_integrator(integrator_name, base_dt, noise_type, noise_val):
    from tvb.simulator.lab import integrators, noise
    temp_integrator = getattr(integrators,integrator_name)
    temp_noise = getattr(noise, noise_type)
    noise = temp_noise(nsig = np.array(noise_val))
    integrator_class = temp_integrator(dt = base_dt, noise = noise)
    return integrator_class


def make_monitors(monitor_type='Raw'):
    from tvb.simulator.lab import monitors
    monitor_class = getattr(monitors,monitor_type)
    return monitor_class


def run_simulation(model, connectivity, out_file, conduction_speed=2.0,
                   simulation=100.):
    from tvb.simulator.lab import simulator
    sim = simulator.Simulator(model=model, connectivity=connectivity)
    sim.configure()
    (time, data), (tavg_time, tavg_data), _ = sim.run()
    np.save(out_file, data)


# https://miykael.github.io/nipype_tutorial/notebooks/basic_function_interface.html
model = Node(
    Function(
        input_names=['model_name', 'parameters'],
        output_names=['model_class'],
        function=make_model
    ),
    name='create_model'
)


connector = Node(
    Function(
        input_names=['weights', 'lengths'],
        output_names=['conn_class'],
        function=make_connectivity
    ),
    name='create_connector'
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
        input_names=['model_input', 'connectivity', 'out_file',
                     'conduction_speed', 'simulation'],
        output_names=['time', 'data'],
        function=run_simulation
    ),
    name='simulate'
)

# https://miykael.github.io/nipype_tutorial/notebooks/basic_workflow.html
workflow = Workflow(name='TVB Demo!!!')
workflow.connect([
    (model, simulate, [("model_class", "model_input")]),
    (connector, simulate, [("conn_class", "connectivity")]),
    (integrator, simulate, [("integrator_class", "integrator_input")]),
    (monitors, simulate, [("monitor_class", "monitor_input")])
])


# NOW DEFINE YOUR INPUTS
# https://miykael.github.io/nipype_tutorial/notebooks/basic_data_input.html
workflow.model.inputs.model_name = 'Generic2dOscillator'
# https://miykael.github.io/nipype_tutorial/notebooks/basic_iteration.html
workflow.model.iterables = ('parameters', [4, 8, 16])
workflow.connector.inputs.weights = None
workflow.connector.inputs.lengths = None
workflow.integrator.inputs.integrator_type = 'HeunStochastic'
workflow.integrator.iterables = ('noise', [1, 2, 3, 4])

workflow.run('MultiProc', plugin_args={'n_procs': 10})