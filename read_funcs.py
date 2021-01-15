import numpy as np



def find_tTot_traj(file):
    i=0
    with open (file) as myfile:

        for line in myfile:
            if "Atoms. Timestep:" in line:
                i+=1

            
    return i 


def find_tot_atoms_traj(file):
    with open(file) as f:
        first_line = f.readline()


    return int(first_line)


def getDims(file):
    d_str = []
    with open (file) as myfile:
        i=0
        for line in myfile:
            if i>0:
                d_str.append(line)
                i+=1
                
            if (i==4):
                break
            if "ITEM: BOX BOUNDS pp pp pp\n" in line:
                i=1
            
    #d_arr = np.array([int(i) for i in d_str])
    d_arr = np.loadtxt(d_str, delimiter = " ")[:,1]
    return d_arr
    


def getTimeArr(file):
    t_str = []
    with open (file) as myfile:
        i=0
        for line in myfile:
            if i==1:
                t_str.append(line)
                i=0
            if "ITEM: TIMESTEP\n" in line:
                i=1
            
    t_arr = [int(i) for i in t_str]
    
    return np.array(t_arr)


def getStressArr(file,tTot,cellNum):
    
    stress_arr  = np.zeros((tTot,cellNum, 9))
    for t in range(tTot):
        i=0
        i_end=t
        cell_str = []
        with open (file) as myfile:
            for line in myfile:

                if ("ITEM: ATOMS" in line) and (i==i_end):
                    break

                if ("ITEM: ATOMS" in line) and (i<i_end):
                    i+=1

            for line in myfile:
                if "ITEM: TIMESTEP" in line:
                    break
                cell_str.append(line)
            
            
        stress_arr[t] = np.array([np.array(cell_str[i].split( )).astype(float) for i in range(len(cell_str))])
        
        
    tens_i = [0,3,4,6,1,5,7,8,2]
    stress_arr = stress_arr[:,:,[tens_i]].reshape((tTot,cellNum, 3,3))


    return stress_arr



    

def getAtomNumber(file):
    i=0
    
    with open (file) as myfile:
        for line in myfile:
            
            if (i==1):
                atomNum = int(line)
                break


            if "ITEM: NUMBER OF ATOMS" in line:
                i = 1
                
    return atomNum
                
                

def getCellArr(file,tTot,cellNum): 
    
    cell_arr  = np.zeros((tTot,cellNum, 3))
    for t in range(tTot):
        i=0
        i_end=t
        cell_str = []
        with open (file) as myfile:
            for line in myfile:

                if ("ITEM: ATOMS" in line) and (i==i_end):
                    break

                if ("ITEM: ATOMS" in line) and (i<i_end):
                    i+=1

            for line in myfile:
                if "ITEM: TIMESTEP" in line:
                    break
                cell_str.append(line)


        cell_arr[t] = np.array([np.array(cell_str[i].split( )[2:]).astype(float) for i in range(len(cell_str))])
    return cell_arr



def getLastCellArr(file,tTot,cellNum):
    cell_arr  = np.zeros((cellNum, 3))

    i=0
    i_end=tTot-1
    cell_str = []
    with open (file) as myfile:
        for line in myfile:

            if ("ITEM: ATOMS" in line) and (i==i_end):
                break

            if ("ITEM: ATOMS" in line) and (i<i_end):
                i+=1

        for line in myfile:
            if "ITEM: TIMESTEP" in line:
                break
            if len(line.split( )[2:])>1:    
                cell_str.append(line)


    cell_arr = np.array([np.array(cell_str[i].split( )[2:]).astype(float) for i in range(len(cell_str))])
    
    return cell_arr


    

def getLastStressArr(file,tTot,cellNum):
    stress_arr  = np.zeros((cellNum, 9))

    i=0
    i_end=tTot-1
    cell_str = []
    with open (file) as myfile:
        for line in myfile:

            if ("ITEM: ATOMS" in line) and (i==i_end):
                break

            if ("ITEM: ATOMS" in line) and (i<i_end):
                i+=1

        for line in myfile:
            if "ITEM: TIMESTEP" in line:
                break
            cell_str.append(line)


    stress_arr = np.array([np.array(cell_str[i].split( )).astype(float) for i in range(len(cell_str))])

        
    tens_i = [0,3,4,6,2,5,7,8,2]
    stress_arr = stress_arr[:,:,[tens_i]].reshape((cellNum, 3,3))
    return stress_arr
    

def last_out_traj(file,tTot,atoms):
    i=0
    cell_str = []

    inter=1
    cell_arr = np.zeros((atoms,3))
    with open (file) as myfile:

        for line in myfile:
            if "Atoms. Timestep:" in line:
                i+=1
                cell_str = []
                ln=0
            if i==tTot:
                if "1 " in line:
                    cell_str.append(line)
                    ln+=1

                if ln==atoms:
                    cell_arr = np.array([np.array(cell_str[i].split( )[1:]).astype(float) for i in range(len(cell_str))])
    return cell_arr




def full_out_traj(file,tTot,atoms,inter = 10):
    i=0
    ln =0
    cell_str = []
    cell_arr = np.zeros((int(tTot/inter),atoms,3))
    with open (file) as myfile:

        for line in myfile:
            if "Atoms. Timestep:" in line:
                i+=1
                cell_str = []
                ln=0
            if i%inter==0:
                if "1 " in line:
                    cell_str.append(line)
                    ln+=1

                if ln==atoms:
                    cell_arr[int(i/inter)-1] = np.array([np.array(cell_str[i].split( )[1:]).astype(float) for i in range(len(cell_str))])

    return cell_arr

            





#def last_out(file,tTot,atoms):

    
    
    