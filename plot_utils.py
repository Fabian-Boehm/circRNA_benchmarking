import plotnine
import utils
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns


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
    plt.yscale('linear')
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


def grouped_absolute_scatterplot_with_individual_bases(data, category_labels, base_values, data_point_labels, title, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    for idx, (group, labels) in enumerate(zip(data, data_point_labels)):
        x_values = np.random.normal(idx + 1, 0.04, size=len(group))  # Adding jitter for better visibility
        ax.scatter(x_values, group, label=category_labels[idx])

        # Plot a base value line for the current group
        ax.axhline(y=base_values[idx], color='black', linestyle='--', linewidth=1, xmin=(idx + 0.75) / len(data), xmax=(idx + 1.25) / len(data))

        # Label each point with its custom label
        for x, y, label in zip(x_values, group, labels):
            ax.text(x, y, f'{label} ({y:.2f})', color='black', fontsize=8, ha='center')

    ax.set_xticks(range(1, len(category_labels) + 1))
    ax.set_xticklabels(category_labels)
    ax.set_title(title)
    plt.legend()
    plt.yscale('linear')
    filename = title.replace(':', '').replace('/', '').strip()
    plt.savefig(f'{filename}.jpg')
    plt.clf()


def tool_comparison_histogram(statnumber, directory, out_dir):
    os.chdir(directory)

    labels = []
    values = []
    title = 'Plotname'

    for file in os.listdir():
        labels.append(file.split('.')[0])
        stat_name, statvalue = get_stat(statnumber, file)
        values.append(float(statvalue[0].strip()))
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

    for file in os.listdir():
        labels.append(file.split('.')[0])
        xlabel, statvalue = get_stat(statnumber1, file)
        x.append(float(statvalue[0].strip()))
        ylabel, statvalue = get_stat(statnumber2, file)
        y.append(float(statvalue[0].strip()))

    os.chdir(out_dir)
    labeled_scatterplot(x=x, y=y, xlabel=xlabel, ylabel=ylabel, labels=labels,
                        title='{}_vs_{}'.format(xlabel, ylabel).replace(':', '').replace('/', '').strip())


def sample_deviation_barplot(statnumber, sample_dir, tool_dir, out_dir):
    tool_files = os.listdir(tool_dir)
    tool_names = [os.path.splitext(file)[0] for file in tool_files]
    data = []
    labels = []
    basevalues = []

    for filename in tool_files:
        sample_file = os.path.join(sample_dir,filename)
        tool_file = os.path.join(tool_dir,filename)
        stat_name, basevalue = get_stat(statnumber, tool_file)
        basevalues.append(float(basevalue[0].strip()))

        _, samples = get_stat(0, sample_file)
        labels.append(samples)
        _, values = get_stat(statnumber, sample_file)
        values = [float(value.strip()) for value in values]
        data.append(values)


    title = stat_name + '_all_samples'
    os.chdir(out_dir)
    grouped_absolute_scatterplot_with_individual_bases(data,tool_names,basevalues,labels,title)
