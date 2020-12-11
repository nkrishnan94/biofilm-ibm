import numpy as np
import glob
import os 
from datetime import datetime


path = os.getcwd()

z_length = np.array([6,12,18])
#x_length = np.array([100,150,200])
#deform_scale = np.array([.5,.7,.9])
                        
time_str = datetime.now()
d=time_str.strftime("%m_%d_%y_%H_%M_%S")
new_path = path+"/sim_files_KA"
samples= 1
try:
    os.mkdir(new_path)
except:
    print("Could not make new directory!")
cnt=1
for z in z_length:
    for n in range(samples):



        time_str = datetime.now()
        d_1=time_str.strftime("%m_%d_%y_%H_%M_%S")
        file_str=str(d_1)+"_thick_"+str(z)+"_len_"+str(200)+"_scale_"+str(.6)+'_rep_'+str(n)
        f = open(new_path+"/biofilm_KA_"+str(cnt)+".inp", "a")
        f.write('#-------------------------- Initial Setup -------------------------------------#\n')
        f.write('log ' +new_path+'/log_KA_'+str(cnt)+'_'+file_str+'.log\n')
        f.write('units       lj\n')
        f.write('atom_style  atomic\n')
        f.write('dimension   3\n')
        f.write('boundary    p p p\n')
        f.write('timestep    0.01\n')
        f.write('#------------------------------------------------------------------------------#\n')
        f.write('#-------------------------- Atomic Setup --------------------------------------#\n')
        f.write('region film block 0 200 0 '+str(z)+' 0 6 \n')# Geometrical region.
        f.write('create_box 2 film \n')# Create simulation box.
        f.write('create_atoms 1 random ' +str(int(6*200*.75*z)) +' '+str(n+1)+' '+'film\n') # Create atoms at random within film.
        f.write('create_atoms 2 random ' +str(int(6*200*.75*z)) +' '+str(10000+n+1)+' '+'film\n') # Create atoms at random within film.
        f.write('neigh_modify every 1 delay 0 check yes\n')

        f.write('mass 1 1\n')
        f.write('mass 2 1\n')
        f.write('pair_style lj/cut 2.5\n') # Define interaction potential.
        f.write('pair_coeff 1 1 1 1 1.5\n')
        f.write('pair_coeff 1 2 1.5 .8 2\n')
        f.write('pair_coeff 2 2 0.5 .88 2.2\n')

        f.write('minimize 1.0e-4 1.0e-6 1000 1000\n')
        f.write('#-------------------------------- Outputs -------------------------------------#\n')
        f.write('thermo 1000\n')
        f.write('thermo_style custom step temp press density ly\n')
        f.write('compute stress all centroid/stress/atom NULL\n')
        f.write('compute press all pressure NULL pair\n')
        f.write('dump 1 all atom 500 ' +new_path+'/traj_KA_'+file_str+'.out\n')
        f.write('dump 3 all atom 500 ' +new_path+'/traj_KA_'+file_str+'.xyz\n')
        f.write('dump_modify 1 sort id append yes\n')
        f.write('dump 2 all custom 500 ' +new_path+'/stress_KA_'+file_str+'.out c_stress[*]\n')

        f.write('#------------------------------------------------------------------------------#\n')
        f.write('#------------------------- Running the Simulation -----------------------------#\n')
        f.write('fix 1 all nve/limit 0.1\n')
        f.write('fix 2 all langevin 2.0 2.0 0.5 1530917 zero yes\n')
        f.write('velocity all create 2.0 4928351 mom yes rot yes dist gaussian\n')
        f.write('run 5000\n')
        f.write('unfix 1\n')
        f.write('unfix 2\n')
        f.write('#------------------------------------------------------------------------------#\n')

        f.write('fix 10 all nvt temp 3 0.1 $(100.0*dt)\n')
        f.write('run 5000\n')
        f.write('unfix 10\n')

        f.write('fix 20 all npt temp 0.1 0.1 $(100.0*dt) y 0 0 $(1000.0*dt)\n')
        f.write('run 5000\n')
        f.write('unfix 20\n')

        f.write('change_box all y final -40 40\n')

        f.write('fix 30 all nvt temp 0.1 0.1 $(100.0*dt)\n')
        f.write('run 10000\n')

        f.write('fix 40 all deform 1 x scale '+str(.6)+' remap x units box \n')
        f.write('run '+str(10000)+' \n')

        f.write('unfix 40\n')
        f.write('run 10000\n')
        f.close()
        cnt+=1
                
files= glob.glob(new_path+'/*.inp')

#for f in files:
#    os.system('lmp_serial -in ' + str(f))
            
           
                    
                    
          