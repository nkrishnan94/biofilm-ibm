import numpy as np
import numpy as np
import glob
import os 
from datetime import datetime


path = os.getcwd()
#establish, open, file
file_str = "potential.table"
f = open(file_str, "a")
f.write('CUSTOM\n')

E = lambda e1,e2,sig,r: 4*(e1* ( (sig/r)**12-(sig/r)**6) +e2*(sig/r)**2)# potential function, modified Leonard Jones potential with an energy barrier for `bond breaking'
F = lambda a,b,sig,r:  -4*(-(12*a*sig**12)/r**13 + (6*a*sig**6)/r**7 - (2*b*sig**2)/r**3)# -dE/dr
#potential function parameters
#e1,e2,sig=3.4,.8, 1 
e1,e2,sig = 2.5,.5, 1  
#e1,e2,sig = 2,.35,1
#note: e2 =0 gives LJ potential with a cutoff
N=10**5
r_min = .0001
r_max = 4
r_space=np.linspace(r_min,4,N)  #range of r values
#write line by line: ID, distance, potential energy, force
f.write('N '+str(N)+'\n\n')
for i,r,E,F in zip(range(len(r_space)),r_space,E(e1,e2,sig,r_space), ## potential
                    F(e1,e2,sig,r_space)):  # force
    f.write(str(i+1) +" " +str(r)+" "+ str(E) +" "+str(F)+"\n")
            
f.close()