#!/usr/bin/env python
# coding: utf-8

import pandas as pd

df = pd.read_excel(r'C:\Users\justi\Downloads\MINE\MINE Test Results.xlsx')
print(df)

# Create New DataFrame For Problem Size vs Time
time_plot = pd.DataFrame().assign(Problem_Size=df['Problem_Size'], Time_Basic=df['Time_Basic'], Time_Efficient=df['Time_Efficient'] )
print(time_plot)

# Create New DataFrame For Problem Size vs Memory
mem_plot = pd.DataFrame().assign(Problem_Size=df['Problem_Size'], Memory_Basic=df['Memory_Basic'], Memory_Efficient=df['Memory_Efficient'] )
print(mem_plot)

import matplotlib.pyplot as m

#time plot
fig, ax = m.subplots()
ax = m.plot(time_plot['Problem_Size'], time_plot['Time_Basic'], marker="^", label='Basic Version')
ax = m.plot(time_plot['Problem_Size'], time_plot['Time_Efficient'], marker="s", label='Efficient Version',linestyle="--")
m.legend(loc='upper left');
m.xlabel('Problem Size (m + n)')
m.ylabel('\nCPU Time (ms)')
m.title('CPU Time vs. Problem Size')
m.subplots_adjust(left=0.05, bottom=0.01)
m.show()
m.savefig('CPU_Plot.jpg')

# memory plot
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Basic'], marker="^", label='Basic Version')
m.plot(mem_plot['Problem_Size'], mem_plot['Memory_Efficient'], marker="s", label='Efficient Version',linestyle="--")
m.legend(loc='upper left');
m.xlabel('Problem Size (m + n)')
m.ylabel('\nMemory Usage (kb)')
m.title('Memory Usage vs. Problem Size')
m.subplots_adjust(left=0.05, bottom=0.01)
m.show()
m.savefig('Memory_Plot.jpg')
