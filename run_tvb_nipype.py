from tvb_interface import *
import sys

graphname, nproc = sys.argv[1:]
nproc = int(nproc)
workflow.write_graph(graph2use='exec', dotfilename='./' + graphname + '.dot')

# run workflow in parallel
print('running workflow...')
print(type(nproc))
#workflow.run('MultiProc', plugin_args={'n_procs': nproc})

