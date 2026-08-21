import os
import socket

main_config = dict()

# change to the name to your own local machine
main_config['local_computer'] = "josecsOmarchy"

# Change dirctory for both local machine and on the cluster
if (socket.gethostname() == main_config['local_computer']):
    #Local machine path
    main_config["main"] = '/home/josecs/Desktop/supereeg_env' # Path where pipeline results will appear
    main_config["starting_data"] = '/home/josecs/Desktop/supereeg_env' # Path for stating npzs data
    main_config["scripts"] = "/home/josecs/miniconda3/envs/supereeg_env/supereeg_JCS/code_hellgate/scripts" # Path where pipeline scripts live
else:
    #Hellgate Cluster path
    main_config["main"] = '/mnt/beegfs/projects/jc158347/supereeg_jcs/supereeg_env' # Path where pipeline results will appear
    main_config["starting_data"] = '/mnt/beegfs/projects/brAIn_lab/datasets/eeg/Berezutskaya_data' # Path for stating npzs data
    main_config["scripts"] = '/mnt/beegfs/projects/jc158347/supereeg_jcs/scripts' # Path where pipeline scripts live