import os
import socket
import sys

# Attach main_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main_config import main_config

config = dict()

config['template'] = 'run_job.sh'

# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======
if socket.gethostname() == main_config['local_computer']:
    config['datadir'] = main_config["starting_data"]
    config['workingdir'] = main_config["main"]+'/bo'
    config['startdir'] = main_config["main"]  # directory to start the job in
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job_local.sh')
else:
    # '/mnt/beegfs/projects/lo243677e/brAIn_lab/data/ecog/RAM'
    config['datadir'] = main_config["starting_data"]
    config['workingdir'] = main_config["main"]+'/bo'
    config['startdir'] = main_config["main"]
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job.sh')

# job creation options
config['scriptdir'] = os.path.join(config['workingdir'], 'scripts')
config['lockdir'] = os.path.join(config['workingdir'], 'locks')
config['resultsdir'] = config['workingdir']

# runtime options
config['jobname'] = "file_io_npz_bo"  # default job name
config['q'] = "default"  # options: default, testing, largeq
config['nnodes'] = 1  # how many nodes to use for this one job
config['ppn'] = 1  # how many processors to use for this one job (assume 4GB of RAM per processor)
config['walltime'] = '02:00:00'  # maximum runtime, in h:MM:SS
#config['startdir'] = '/ihome/lowen/repos/supereeg/examples'  # directory to start the job in
config['cmd_wrapper'] = "python"  # replace with actual command wrapper (e.g. matlab, python, etc.)
config['modules'] = "(\"python/3.13\")"  # separate each module with a space and enclose in (escaped) double quotes
# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======

