#download LAMMPS
git clone --depth=1 https://github.com/lammps/lammps.git
cd lammps

#load the CSD3 modules for CPU/KNL architectures
module purge
module load rhel7/default-peta4

#switch to the src directory
cd src

#activate the user-reaxc package
make yes-user-reaxc

#compile lammps with mpi support
make mpi