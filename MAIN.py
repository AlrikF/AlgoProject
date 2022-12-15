import subprocess
import sys

#lists for storing values from output files. Values will be ordered for input1 file to input15
Eff_Memory =[]
Eff_Time =[]
Problem_Size=[]
Basic_Memory=[]
Basic_Time=[]

#ensure path is correct

#loop 15 times for 15 testcases
for i in range(1,16):
    j=str(i)
    path='python Efficient_Algorithm.py' + ' ./datapoints/in' + j + '.txt' + ' e_output' + j + '.txt'
    cmd = path
    p = subprocess.Popen(cmd, shell=True)
    out, err= p.communicate()
    print(err)
    print(out)
    #change the path
    outpath = r"./e_output" + j + '.txt'
    file=open(outpath)
    content=file.readlines()

    print(content)
    m=content[4]
    s1=content[1].replace("_","")
    s2=content[2].replace("_","")
    t=content[3]

    #slen= len(s)

    # Slice string to remove last 2 characters from string
    #s=s[:slen - 2]
    #s=int(s)
    tlen= len(t)
    t=t[:tlen - 1]
    t=float(t)
    m=int(m)
    Eff_Memory.append(m)
    Eff_Time.append(t)
    Problem_Size.append(len(s1)+len(s2)-2)
    # end of running efficient code, all 15 test cases

    path='python Basic_Algorithm.py' + ' ./datapoints/in' + j + '.txt' + ' b_output' + j + '.txt'
    cmd = path
    p = subprocess.Popen(cmd, shell=True)
    out, err= p.communicate()
    print(err)
    print(out)
    #change the path
    outpath = r"./b_output" + j + '.txt'
    file=open(outpath)
    content=file.readlines()
    m=content[4]

    #s1=content[1].replace("-","")
    #s2=content[2].replace("-","")
    t=content[3]
    #slen= len(s)

    # Slice string to remove last 2 characters from string
    #s=s[:slen - 2]
    #s=int(s)
    tlen= len(t)
    t=t[:tlen - 1]
    t=float(t)
    m=int(m)
    Basic_Memory.append(m)
    Basic_Time.append(t)
    #Problem_Size.append(len(s1)+len(s2)-4)
    print('\nTestcase ' + j + ' complete!\n')
    #end of running basic.py for all 15 input files


from collections import OrderedDict
d = OrderedDict()
for i in range(len(Problem_Size)):
    d[Problem_Size[i]] = [Basic_Memory[i], Eff_Memory[i]]

print(d)
ps = []
bm = []
em = []
for key,value in d.items():
    ps.append(key)
    bm.append(value[0])
    em.append(value[1])

#create dicionary
Memory_Plot = {}
#append lists to dictionary
Memory_Plot["Problem_Size"] = ps
Memory_Plot["Memory_Basic"] = bm
Memory_Plot["Memory_Efficient"] = em
print(len(Problem_Size), len(Basic_Memory), len(Eff_Memory))
CPU_Plot={}
CPU_Plot["Problem_Size"] = Problem_Size
CPU_Plot["Time_Basic"] = Basic_Time
CPU_Plot["Time_Efficient"] = Eff_Time

# the above two dictionaries will be used to create two dataframes which will then be used to plot our graphs

import pandas as pd
mem_plot = pd.DataFrame(Memory_Plot)
time_plot= pd.DataFrame(CPU_Plot)

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
#fig, ax = m.subplots()
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Basic'], marker="^", label='Basic Version')
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Efficient'], marker="s", label='Efficient Version',linestyle="--")

#ax2 = m.gca()
#ax2.set_ylim([5000, 25000])
m.legend(loc='upper left')
m.xlabel('Problem Size (m + n)')
m.ylabel('\nMemory Usage (kb)')
m.title('Memory Usage vs. Problem Size')
m.subplots_adjust(left=0.05, bottom=0.01)
m.show()
m.savefig('Memory_Plot.jpg')



print("\n Basic Time:: ")
print(Basic_Time)
print("\n Efficient Time:: ")
print(Eff_Time)
print("\n Basic Memory :: ")
print(bm)
print("\n Efficient Memory :: ")
print(em)
print("\n Problem Size::", ps)

