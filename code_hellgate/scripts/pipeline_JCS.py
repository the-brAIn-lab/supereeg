import supereeg as se
import sh
import socket
import time
import numpy as np
import os
import json
from main_config import main_config

if socket.gethostname() == main_config["local_computer"]:
    supereeg_env = main_config["main"]
    fileIO_jobsubmit_path = main_config["scripts"]+"/file_io/file_io_job_submit.py"
    pyFR_jobsubmit_path = main_config["scripts"]+"/pyFR_locs/union_locs_job_submit.py"
    fullmats_jobsubmit_path = main_config["scripts"]+"/full_mats/full_mats_job_submit.py"
    avemats_jobsubmit_path = main_config["scripts"]+"/ave_mats/ave_mats_job_submit.py"
    reacon_jobsubmit_path = main_config["scripts"]+"/recon/recon_job_submit.py"
else:
    supereeg_env = main_config["main"]
    fileIO_jobsubmit_path = main_config["scripts"]+"/file_io/file_io_job_submit.py"
    pyFR_jobsubmit_path = main_config["scripts"]+"/pyFR_locs/union_locs_job_submit.py"
    fullmats_jobsubmit_path = main_config["scripts"]+"/full_mats/full_mats_job_submit.py"
    avemats_jobsubmit_path = main_config["scripts"]+"/ave_mats/ave_mats_job_submit.py"
    reacon_jobsubmit_path = main_config["scripts"]+"/recon/recon_job_submit.py"

run = sh.Command('python')

# This the file which compiles pipeline output stats and stores it in csv_file
pipeline_output_py = "/mnt/beegfs/projects/jc158347/supereeg_jcs/test_code/result_output_analysis.py"

### Change code below to adjust analysis ######
# default parameters for density kernal: {'n_neighbors' : 15, 'tau' : 0.05, 'sigma': 0.01, 'max':5}
# default parameters for stationary kernal: {'rbf_width': 20}
kernal = "stationary"
apply_motif = ["False","True"]
parms = [{'rbf_width': 5},{'rbf_width': 5}]
# This the file which compiles pipeline output stats and stores it in csv_file
pipeline_output_py = "/mnt/beegfs/projects/jc158347/supereeg_jcs/test_code/result_output_analysis.py"
csv_file = "/mnt/beegfs/projects/jc158347/supereeg_jcs/pipeline_output_stats.csv"
run_type = f"kernal-{kernal}_data-berk_task-rest"
#############################################

for i in range(len(parms)):
    print("Running File_IO: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    start_time_fileIO = time.time()
    run(fileIO_jobsubmit_path)
    end_time_fileIO = time.time()
    elapsed_time_fileIO = end_time_fileIO - start_time_fileIO
    print("Done running File_IO: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    print(f"Total run time {elapsed_time_fileIO} sec\n")

    run_time = np.array([elapsed_time_fileIO])
    np.savez(supereeg_env+"/Total_Run_Time.npz",run_time)

    print("Running pyFR: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    start_time_pyFR = time.time()
    run(pyFR_jobsubmit_path)
    end_time_pyFR = time.time()
    elapsed_time_pyFR = end_time_pyFR - start_time_pyFR
    print("Done running pyFR: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    print(f"Total run time {elapsed_time_pyFR} sec\n")

    run_time = np.array([elapsed_time_fileIO,elapsed_time_pyFR])
    np.savez(supereeg_env+"/Total_Run_Time.npz",run_time)

    print(f"Running Full_Mats: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    start_time_fullmats = time.time()
    run(fullmats_jobsubmit_path, kernal,f"'''{parms[i]}'''",apply_motif[i])
    end_time_fullmats = time.time()
    elapsed_time_fullmats = end_time_fullmats - start_time_fullmats
    print(f"Done running Full_mats: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    print(f"Total run time {elapsed_time_fullmats} sec\n")

    run_time = np.array([elapsed_time_fileIO,elapsed_time_pyFR,elapsed_time_fullmats])
    np.savez(supereeg_env+"/Total_Run_Time.npz",run_time)

    print(f"Running Ave_mats: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    start_time_avemats = time.time()
    run(avemats_jobsubmit_path, kernal,f"'''{parms[i]}'''",apply_motif[i])
    end_time_avemats = time.time()
    elapsed_time_avemats = end_time_avemats - start_time_avemats
    print(f"Done running Ave_mats: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    print(f"Total run time {elapsed_time_avemats} sec\n")

    run_time = np.array([elapsed_time_fileIO,elapsed_time_pyFR,elapsed_time_fullmats,elapsed_time_avemats])
    np.savez(supereeg_env+"/Total_Run_Time.npz",run_time)

    print(f"Running Recon: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    start_time_recon = time.time()
    run(reacon_jobsubmit_path, kernal,f"'''{parms[i]}'''",apply_motif[i])
    end_time_recon = time.time()
    elapsed_time_recon = end_time_recon - start_time_recon
    print(f"Done running Recon: kernal="+ " "+kernal+" with parameters "+str(parms[i]))
    print(f"Total run time {elapsed_time_recon} sec\n")

    run_time = np.array([elapsed_time_fileIO,elapsed_time_pyFR,elapsed_time_fullmats,elapsed_time_avemats,elapsed_time_recon])
    #run_time = np.array([elapsed_time_recon])
    np.savez(supereeg_env+"/Total_Run_Time.npz",run_time)

    #Compile pipeline stats
    run_type = run_type+f"_{apply_motif[i]}Motif"
    run(pipeline_output_py,run_type,csv_file,supereeg_env,kernal)

    new_name = supereeg_env + "_"+ kernal+"_"+str(parms[i])+"_motif"+apply_motif[i]
    os.rename(supereeg_env, new_name)
    os.mkdir(supereeg_env)