#!/bin/bash -l

# DO NOT MODIFY THIS FILE!
# MODIFY config.py AND create_and_submit_jobs.py AS NEEDED

#SBATCH --job-name=ave_mats_submit

#SBATCH --output=ave_mats_out%A_%a.out
#SBATCH --error=ave_mats_err%A_%a.err

#SBATCH --output=/mnt/beegfs/projects/jc158347/supereeg_jcs/scripts/ave_mats/ave_mats_out.txt
#SBATCH --error=/mnt/beegfs/projects/jc158347/supereeg_jcs/scripts/ave_mats/ave_mats_err.txt


#SBATCH --nodes=1

#SBATCH --cpus-per-task=3

#SBATCH --mem-per-cpu=10gb

#SBATCH --mail-type=END,FAIL

#SBATCH --mail-user=jose.carmona-sanchez@umconnect.umt.edu

source /opt/conda/etc/profile.d/conda.sh

conda activate supereeg_env

# set the working directory *of the job* to the specified start directory

python /mnt/beegfs/projects/jc158347/supereeg_jcs/scripts/ave_mats/ave_mats_job_submit.py density '''{'n_neighbors': 15, 'tau': 0.05, 'sigma': 0.01, 'max': 5}'''