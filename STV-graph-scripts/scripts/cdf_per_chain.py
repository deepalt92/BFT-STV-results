"""
Cumulative Distribution Function of Latency
-------------------------------------------

Simple graph returning the CDF of the latencies of transactions
when presented in a workload.
"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List
import itertools
import numpy
import matplotlib.legend as mlegend

from utils import DiabloChainOutputResult, colors

##### CONSTANT
FAIL_LATENCY = 1_000_000 # Latency to indicate a failure

def generate_cdf_graph(dataset: List[DiabloChainOutputResult], title: str, x_label: str, y_label: str, output_file=None) -> None:
    """
    Generates the CDF of latencies for transactions.
    Output is either displayed (if output file is None), else saved as output_file

    :param dataset - The list of results
    :param title - The graph title
    :param x_label - The x label for the graph
    :param y_label - The y label for the graph
    """

    if (len(dataset) == 0):
        return

    max_xlim = 0

    # Total latencies (all the latencies added into a list)
    latencies_total = {x.name: [] for x in dataset}

    # Collect the data and store in the latencies
    for chain in dataset:
        run_latencies = {}
        latency_count = 0

        for iteration in chain.data:
            # Add all the latencies
            if iteration['SecondaryResults'] is not None:
                secondary_latencies = map(lambda l: l['TxLatencies'], iteration['SecondaryResults'])
                chained_latencies = itertools.chain.from_iterable(secondary_latencies)
                all_latencies = list(map(lambda x: x / 1000, filter(lambda x: x > 0, chained_latencies)))
                if len(all_latencies) > 0:
                    latencies_total[chain.name] += [i for i in all_latencies]
                    # latencies_per_run[chain.name].append([i for i in iteration["AllTxLatencies"]])

                    max_xlim = max(max_xlim, max(all_latencies))

                # Add '10000' for
                latencies_total[chain.name] += [FAIL_LATENCY for i in range(iteration["TotalFails"])]


    # Format for the data frame
    # Total latency formatted has the [chain, latency_value]
    total_latencies_formatted = []
    for chain in latencies_total:
        total_latencies_formatted += [[chain, i] for i in latencies_total[chain]]

    #sns.set_style("whitegrid")
    sns.set_style("ticks")

    df = pd.DataFrame(
        data=total_latencies_formatted[:668],
        columns=["chain", "latency"]
    )
    orderedlatencies=[]
    i=0
    data=total_latencies_formatted[:668]
    while i < len(data):
        orderedlatencies.append(data[i][1])
        i=i+1
        
    print(orderedlatencies)
    print(len(orderedlatencies))
    #print(orderedlatencies.sort())
    #print(orderedlatencies[131])
    #print(orderedlatencies[132])

    #diff=[]

    #i=0
    #while i < len(orderedlatencies)-1:
    #    diff.append(orderedlatencies[i+1]-orderedlatencies[i])
    #    i=i+1
    #diff.sort()
    #print(diff)
    fig = matplotlib.pyplot.gcf()
    font = {'size': 40}
    matplotlib.rc('font', **font)

    #palette = sns.color_palette('Dark2', n_colors=7, desat=0.8)

    #change this plot to a tower plot
    #plt.hist(orderedlatencies)
    k=1
    i=1
    listD=[]
    while k < 669:
        if k==167*i:
            listD.append(k)
            i=i+1
        k=k+1

    j=0
    i=1
    vals=[]
    while j < 669:
        if j==167*i:
            vals.append(orderedlatencies[j-1])
            i=i+1
        j=j+1    
    plt.bar(listD, vals)
    """
    ax = sns.ecdfplot(
        data=df,
        x="latency",
        hue="chain",
	#palette=sns.blend_palette(colors=palette, n_colors=7, input='rgb'),
        palette=colors,
        linewidth=2,
        legend=False,
	#marker='^', ls='-',
    )
    """
    #ax.legend(loc='best', bbox_to_anchor=(0, 0))
    #leg = ax.get_legend()
    #ax.legend(ncol=6)
    #mlegend.Legend(ax, ncol=2)
    #matplotlib.rcParams["legend.fancybox"] 
    #leg.set_title(None)
    
    #plt.xlim(0, max_xlim + 20)
    plt.xlim(3, 700)
    #plt.xticks(numpy.arange(1, 669, 168))
    fig.set_size_inches(16, 10)
    # make figure flat
    #plt.rcParams["figure.figsize"] = (14,5)
    # plt.legend('',frameon=False)
    plt.xlabel("transaction number")
    plt.ylabel("latency (seconds)")


    # remove top and right axes
    # sns.despine()    

    # ax.set_title(title)
    #ax.set_ylabel(y_label)
    #ax.set_xlabel(x_label)

    plt.tight_layout()

    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file, format='pdf')

    plt.close()
