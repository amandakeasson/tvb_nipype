def load_connectivity_mat(in_file, normalize=False):
     import scipy.io
     datamat = scipy.io.loadmat(in_file)
     sc_weights = datamat['sc_weights']
     if normalize:
         sc_weights = sc_weights / sc_weights.max()
     tract_lengths = datamat['tract_lengths']
     return sc_weights, tract_lengths


def make_connectivity(weights, lengths):
    from tvb.simulator.lab import connectivity
    conn_class = connectivity.Connectivity(weights=weights, tract_lengths=lengths)
    return conn_class



from nipype import Node, Function

sc_loader = Node(
    Function(
        input_names=['in_file', 'normalize'],
        output_names=['sc_weights', 'tract_lengths'],
        function=load_connectivity_mat
    ),
    name='load_sc_mat'
)


connector = Node(
    Function(
        input_names=['weights', 'lengths'],
        output_names=['conn_class'],
        function=make_connectivity
    ),
    name='create_connector'
)

