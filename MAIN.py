import subprocess

#lists for storing values from output files. Values will be ordered for input1 file to input15
Eff_Memory=[]
Eff_Time=[]
Problem_Size=[]
Basic_Memory=[]
Basic_Time=[]

#ensure path is correct

#loop 15 times for 15 testcases
for i in range(1,16):
    j=str(i)
    path='python Efficient_Algorithm.py' + ' in' + j + '.txt' + ' e_output' + j + '.txt'
    cmd = path
    p = subprocess.Popen(cmd, shell=True)
    out, err= p.communicate()
    print(err)
    print(out)
    #change the path
    outpath = r"C:\Users\justi\e_output" + j + '.txt'
    file=open(outpath)
    content=file.readlines()
    m=content[4]
    s=content[0]
    t=content[3]
    slen= len(s)
    # Slice string to remove last 2 characters from string
    s=s[:slen - 2]
    s=int(s)
    tlen= len(t)
    t=t[:tlen - 1]
    t=float(t)
    m=int(m)
    Eff_Memory.append(m)
    Eff_Time.append(t)
    Problem_Size.append(s)
    # end of running efficient code, all 15 test cases

    path='python Basic_Algorithm.py' + ' in' + j + '.txt' + ' b_output' + j + '.txt'
    cmd = path
    p = subprocess.Popen(cmd, shell=True)
    out, err= p.communicate()
    print(err)
    print(out)
    #change the path
    outpath = r"C:\Users\justi\b_output" + j + '.txt'
    file=open(outpath)
    content=file.readlines()
    m=content[6]
    s=content[2]
    t=content[5]
    slen= len(s)
    # Slice string to remove last 2 characters from string
    s=s[:slen - 2]
    s=int(s)
    tlen= len(t)
    t=t[:tlen - 1]
    t=float(t)
    m=int(m)
    Basic_Memory.append(m)
    Basic_Time.append(t)
    #Problem_Size.append(s)
    print('\nTestcase ' + j + ' complete!\n')
    #end of running basic.py for all 15 input files


#create dicionary 
Memory_Plot = {}
#append lists to dictionary
Memory_Plot["Problem_Size"] = Problem_Size
Memory_Plot["Memory_Basic"] = Basic_Memory
Memory_Plot["Memory_Efficient"] = Eff_Memory

CPU_Plot={}
CPU_Plot["Problem_Size"] = Problem_Size
CPU_Plot["Time_Basic"] = Basic_Time
CPU_Plot["Time_Efficient"] = Eff_Time

# the above two dictionaries will be used to create two dataframes which will then be used to plot our graphs

import pandas as pd
mem_plot = pd.DataFrame(Memory_Plot)
mem_plot
time_plot= pd.DataFrame(CPU_Plot)
time_plot

import matplotlib.pyplot as m

#time
fig, ax = m.subplots()
ax = m.plot(time_plot['Problem_Size'], time_plot['Time_Basic'], marker="^", label='Basic Version')
ax = m.plot(time_plot['Problem_Size'], time_plot['Time_Efficient'], marker="s", label='Efficient Version',linestyle="--")
m.legend(loc='upper left')
m.xlabel('Problem Size (m + n)')
m.ylabel('\nCPU Time (ms)')
m.title('CPU Time vs. Problem Size')
m.subplots_adjust(left=0.05, bottom=0.01)
m.show()
m.savefig('CPU_Plot.jpg')

# memory
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Basic'], marker="^", label='Basic Version')
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Efficient'], marker="s", label='Efficient Version',linestyle="--")
m.legend(loc='upper left')
m.xlabel('Problem Size (m + n)')
m.ylabel('\nMemory Usage (kb)')
m.title('Memory Usage vs. Problem Size')
m.subplots_adjust(left=0.05, bottom=0.01)
m.show()
m.savefig('Memory_Plot.jpg')
