import plotnine
import utils
import matplotlib.pyplot as plt
import os
import numpy as np


def get_stat(statnumber, filename):
    with open(filename, 'r') as file:
        out = []
        c = 0
        stat_name = ''
        for line in file:
            if line.startswith('#'):
                c = 0
            if c == statnumber:
                line = line.split('\t')
                out.append(line[1])
                stat_name = line[0]
            c += 1
    return stat_name, out


def one_stat_histogramm(labels, values, title):
    plt.bar(range(len(labels)), values)  # Creating a bar graph
    plt.title(title)  # Setting the title
    filename = title.replace(':', '').replace('/', '').strip()
    plt.xticks(range(len(labels)), labels)  # Setting x-axis labels
    plt.xticks(rotation=15)
    plt.savefig('{}.jpg'.format(filename))  # Saving the plot as an image file
    plt.clf()


def labeled_scatterplot(x, y, labels, title='Scatter Plot', xlabel='X-axis', ylabel='Y-axis'):
    fig, ax = plt.subplots()
    ax.scatter(x, y, marker='o', color='blue', alpha=0.6)  # Directly plotting without assignment
    # Adding labels to each point
    for i, label in enumerate(labels):
        ax.annotate(label, (x[i], y[i]))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.grid(True)
    filename = title.replace(':', '').replace('/', '').strip()
    plt.savefig('{}.jpg'.format(filename))
    plt.clf()


def deviation_bar_chart(values, labels, base_value, title):
    """
    Plots a deviation bar chart.

    Parameters:
    - values: list of numerical values
    - labels: list of labels corresponding to the values
    - base_value: the base value for deviation comparison
    """
    deviations = [v - base_value for v in values]

    fig, ax = plt.subplots()
    ax.bar(labels, deviations, color=['green' if x >= 0 else 'red' for x in deviations])

    # Add a line for the base value
    ax.axhline(0, color='black', linewidth=0.8)

    std_dev = np.std(values)
    ax.axhline(std_dev, color='blue', linestyle='--', label='Std. Deviation +')
    ax.axhline(-std_dev, color='blue', linestyle='--', label='Std. Deviation -')


    ax.set_ylabel('Deviation from Base Value')
    ax.set_title('Deviation Bar Chart')
    plt.legend()
    plt.grid(True)
    filename = title.replace(':', '').replace('/', '').strip()
    plt.savefig('{}.jpg'.format(filename))
    plt.clf()


def tool_comparison_histogram(statnumber, directory, out_dir):
    os.chdir(directory)

    labels = []
    values = []
    title = 'Plotname'

    for file in os.listdir():
        labels.append(file.split('.')[0])
        stat_name, statvalue = get_stat(statnumber, file)
        values.append(statvalue[0])
        title = stat_name

    os.chdir(out_dir)
    one_stat_histogramm(labels, values, title)


def tool_comparison_scatterplot(statnumber1, statnumber2, directory, out_dir):
    os.chdir(directory)
    xlabel = ''
    ylabel = ''

    labels = []
    x = []
    y = []
    title = 'Plotname'

    for file in os.listdir():
        labels.append(file.split('.')[0])
        xlabel, statvalue = get_stat(statnumber1, file)
        x.append(statvalue[0])
        ylabel, statvalue = get_stat(statnumber2, file)
        y.append(statvalue[0])

    os.chdir(out_dir)
    labeled_scatterplot(x=x, y=y, xlabel=xlabel, ylabel=ylabel, labels=labels,
                        title='{}_vs_{}'.format(xlabel, ylabel).replace(':', '').replace('/', '').strip())

def sample_deviation_barplot (statnumber, samplesfile, tool_statfile,out_dir):
    toolname = str(tool_statfile).split('/').pop()
    toolname = toolname.split('.')[0]
    stat_name, basevalue = get_stat(statnumber, tool_statfile)
    title = toolname + "_" + stat_name + '_all_samples'

    _, samples = get_stat(0, samplesfile)
    _, values = get_stat(statnumber,samplesfile)

    os.chdir(out_dir)
    deviation_bar_chart(values,samples,basevalue,title)
