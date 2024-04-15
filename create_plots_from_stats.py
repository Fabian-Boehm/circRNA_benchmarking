import utils
import matplotlib.pyplot as plt
import os
import subprocess

plotdir = r"C:\Junk\Hiwi_List\plots"
tool_list = ['circexplorer2', 'circrna_finder', 'ciriquant', 'dcc', 'find_circ', 'segemehl']
stats = utils.read_file_to_array(r"C:\Junk\Hiwi_List\plots\benchmarking_results.txt")
os.chdir(plotdir)

#Globals
statcount = 7
#End: Globals

for i in range(0, 8):
    if i % statcount == 0: continue
    values = []
    stat_floats = []
    statname = ''
    stat = utils.get_stat_from_stats(stats,i)
    c = 0
    while c < len(stat):
        s = stat[c]
        statname = s[0]
        stat_floats.append(float(s[1].replace('%', '').strip()))
        if c % 2 == 1:
            values.append((stat_floats[c] + stat_floats[c - 1]) / 2)
        c += 1

    plt.bar(range(len(tool_list)), values)  # Creating a bar graph
    plt.title(statname)  # Setting the title
    statname = statname.replace(':','').replace('/','').strip()
    plt.xticks(range(len(tool_list)), tool_list)  # Setting x-axis labels
    plt.xticks(rotation= 15)
    plt.savefig(f'{statname}.jpg')  # Saving the plot as an image file
    plt.clf()



print('execution finished!')
