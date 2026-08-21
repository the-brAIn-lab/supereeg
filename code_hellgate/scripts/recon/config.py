import os
import socket
import sys

# Attach main_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main_config

config = dict()

config['template'] = 'run_job.sh'

# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======
if (socket.gethostname() == main_config['local_computer']):
    config['datadir'] =  main_config["main"]+'/bo'
    config['workingdir'] =  main_config["main"]+'/recon'
    config['startdir'] =  main_config["main"]  # directory to start the job in
    config['modeldir'] =  main_config["main"]+'/full_mats/results/union'
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job_local.sh')
else:
    config['datadir'] =  main_config["main"]+'/bo'
    config['workingdir'] =  main_config["main"]+'/recon'
    config['startdir'] =  main_config["main"]  # directory to start the job in
    config['modeldir'] =  main_config["main"]+'/full_mats/results/union'
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job.sh')

# job creation options
config['scriptdir'] = os.path.join(config['workingdir'], 'scripts')
config['lockdir'] = os.path.join(config['workingdir'], 'locks')
config['resultsdir'] = os.path.join(config['workingdir'], 'results')
config['avedir'] = os.path.join(config['startdir'], 'ave_mats/results')
config['og_bodir'] = config['datadir']

# runtime options
config['jobname'] = "recon"  # default job name
config['q'] = "default"  # options: default, testing, largeq
config['nnodes'] = 1  # how many nodes to use for this one job
config['feature'] = 'celln'
config['ppn'] = 16  # how many processors to use for this one job (assume 4GB of RAM per processor)
config['walltime'] = '50:00:00'  # maximum runtime, in h:MM:SS
config['cmd_wrapper'] = "python"  # replace with actual command wrapper (e.g. matlab, python, etc.)
config['modules'] = "(\"python/3.13\")"  # separate each module with a space and enclose in (escaped) double quotes
# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======
