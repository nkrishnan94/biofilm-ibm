#!/bin/bash
#!
#! Example SLURM job script for Peta4-KNL (KNL 7210)
#! Last updated: Mon 13 Nov 12:17:14 GMT 2017
#!

#!#############################################################
#!#### Modify the options in this section as appropriate ######
#!#############################################################

#! sbatch directives begin here ###############################
#! Name of the job:
#SBATCH -J run_sims_LJ
#! Which project should be charged (NB Peta4-KNL projects end in '-KNL'):
#SBATCH -A FUSCO-SL3-CPU
#! Number of nodes to be allocated for the job (for single core jobs always leave this at 1)
#SBATCH --nodes=1
#! Number of tasks. By default SLURM assumes 1 task per node and 1 CPU per task. (for single core jobs always leave this at 1)
#SBATCH --ntasks=1
#! How many many cores will be allocated per task? (for single core jobs always leave this at 1)
#SBATCH --cpus-per-task=1
#! How much wallclock time will be required?
#SBATCH --time=3:00:00
#! Estimated maximum memory needed (job is force-stopped if exceeded):
#! Submit a job array with index values between 0 and 31
#! NOTE: This must be a range, not a single number (i.e. specifying '32' here would only run one job, with index 32)
#SBATCH --mem=5980mb
#SBATCH --array=1-100

#! This is the partition name.
#SBATCH -p skylake

#! mail alert at start, end and abortion of execution
#! emails will default to going to your email address
#! you can specify a different email address manually if needed.
##SBATCH --mail-type=ALL

#! Don't put any #SBATCH directives bselow this line

#! Modify the environment seen by the application. For this example we need the default modules.
. /etc/profile.d/modules.sh                # This line enables the module command
module purge                               # Removes all modules still loaded
module load rhel7/default-peta4            # REQUIRED - loads the basic environment
module load intel/bundles/complib/2017.4
module load gcc-5.4.0-gcc-4.8.5-fis24gg
module load gcc-7.2.0-gcc-4.8.5-pqn7o2k

#! The variable $SLURM_ARRAY_TASK_ID contains the array index for each job.
#! In this example, each job will be passed its index, so each output file will contain a different value

echo "This is job" $SLURM_ARRAY_TASK_ID

#! Command line that we want to run:
#sh lammps_install.sh 
cd /home/npk28/lammps_ibm/sim_files_LJ
export PATH="/home/npk28/lammps_ibm/lammps/src"
lmp_serial -in biofilm_LJ_$SLURM_ARRAY_TASK_ID.inp

