"""
Transactions over time
----------------------

Simple graph returned to represent the transactions over time.

X-axis is represented as a timeseries
Y-axies is the number of transactions that had been committed at that point in time.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List

from utils import DiabloChainOutputResult, colors

def generate_tps_graph(dataset: List[DiabloChainOutputResult], title: str, x_label: str, y_label: str, baseline=None, output_file=None, kernel_size=1) -> None:
    """
    Generates the transaction per second graph.
    Output is either displayed (if output_file is None), else saved as output_file

    :param dataset - The DIABLO datasets.
    :param title - The graph title
    :param x_label - The x label for the graph
    :param y_label - The y label for the graph
    """

    formatted_data = []

    # Go through each chain in the dataset
    for chain in dataset:
        # Formatted data = [chain, iteration, throughput_value, time_value]
        for run_num, data in enumerate(chain.data):
            if data['SecondaryResults'] is not None:
                secondary_throughputs = map(lambda l: l['ThroughputSeconds'], data['SecondaryResults'])
                zipped_throughputs = zip(*secondary_throughputs)
                throughputs = list(map(sum, zipped_throughputs))
                if kernel_size > 1:
                    kernel = np.ones(kernel_size) / kernel_size
                    throughputs = np.convolve(throughputs, kernel, mode='same')
                for time_iter, throughput in enumerate(throughputs):
                    formatted_data.append([
                        chain.name,
                        run_num,
                        throughput,
                        time_iter,
                    ])

    # Format as a data frame
    df = pd.DataFrame(
        data=formatted_data,
        columns=[
            "chain",
            "iteration",
            "throughput",
            "seconds"
        ]
    )

    # Plot Options
    #sns.set_style("whitegrid")
    sns.set_style("ticks")
    fig = matplotlib.pyplot.gcf()
    font = {'size': 22}
    matplotlib.rc('font', **font)
    # Plot the lines
    ax = sns.lineplot(
        data=df,
        x="seconds",
        y="throughput",
        hue="chain",
        palette=colors,
        linewidth=1.5,
        legend=False
    )
    #ax.get_legend().set_title(None)


    # Change this to augment the figure size
    fig.set_size_inches(10, 4)
    plt.xlim(0, 22)
    plt.ylim(0, 4000)
    plt.xlabel("")
    plt.ylabel("")

    # ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    plt.tight_layout()

    if (output_file is None):
        plt.show()
    else:
        plt.savefig(output_file)
    plt.close()
