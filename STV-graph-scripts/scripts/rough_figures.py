#!/usr/bin/env python

"""
Per-Workload (community, company, elitist, toy)

Produces 3 graphs - TPS over time; Stats compared for chain; CDF
"""
import json
import logging
import os
import sys

import matplotlib.colors

import matplotlib.pyplot as plt
import utils
import tps_time
import cdf_per_chain as cdf_latencies

#plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
#plt.rcParams['text.usetex'] = True
# use LaTeX to manage layout
#plt.rcParams['text.usetex'] = 'true'
# override fonts
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = 'Times'

plt.rcParams['font.size'] = '22'
# make figure flatter
plt.rcParams["figure.figsize"] = (10,4)

# remove top and right axes
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False

ALL_COLOURS = list(matplotlib.colors.CSS4_COLORS)

WORKLOADS = ["logs"]
#WORKLOADS = ["community", "company", "elitist", "toy"]
# WORKLOADS = ["amazon", "apple", "dota2000", "facebook", "football", "gafam", "google", "microsoft", "uber", "youtube"]

#if (len(sys.argv) < 2):
#    print("[INVALID base dir] -- usage: python rough_figures.py /path/to/results/dir")
#    print("Example: python figs/rough_figures.py /home/testuser/Diablo/results/")
#    sys.exit(1)

#base = sys.argv[1]
#print(base)
base="C:/Users/dten6395/Desktop/Personal-Dev-stuff/BFT-STV-results/STV-scripts"
# Main function to run
def main():

    if not os.path.isdir("results_figures"):
        os.mkdir("results_figures")

    all_results = {w: {} for w in WORKLOADS}

    # Iterate through workload (community, company ..)
    for workload in WORKLOADS:
        workload_number = list(filter(lambda x: '.DS_Store' not in x, os.listdir(os.path.join("c:",base, workload))))
        all_results[workload] = {wn: {} for wn in workload_number}


        # Get the workload number (100, 1000, 100000....)
        for wn in workload_number:
            print(wn)
            # Find the result directory
            for res_dir in filter(lambda x: ".tar.gz" not in x and '.DS_Store' not in x, os.listdir(os.path.join("c:", base, workload, wn))):

                # Filter out non-result files
                for filename in filter(lambda x: "_results.json" in x, os.listdir(os.path.join("c:",base, workload, wn, res_dir))):

                    # First step, read the name of the chain
                    current_name = ""
                    with open(os.path.join("c:", base, workload, wn, res_dir, "name.txt"), 'r') as f:
                        current_name = ''.join(f.readlines()).strip()

                    # Then read the data
                    data = None
                    with open(os.path.join("c:", base, workload, wn, res_dir, filename), 'r') as f:
                        data = json.load(f)

                    print(wn) 
		    #if current_name == 'algorand':
                    #    continue

                    if current_name not in all_results[workload][wn]:
                        all_results[workload][wn][current_name] = utils.DiabloChainOutputResult(name=current_name, data=[data])
                    else:
                        all_results[workload][wn][current_name].add_iteration(data)

                    # Add the data back to that chain for that workload

    # Let's create the figures

    # TPS over time
    #for w in all_results:
    #    for iteration in all_results[w]:
    #        tps_time.generate_tps_graph(
    #            [all_results[w][iteration][x] for x in all_results[w][iteration]],
    #            "TPS {} {}".format(w, iteration),
    #            "Time (s)",
    #            "Throughput (TPS)",
    #            output_file=f"results_figures/{w}_{iteration}_throughput_time",
    #		kernel_size=3
    #        )

    # CDF of latency
    for w in all_results:
        for iteration in all_results[w]:
            cdf_latencies.generate_cdf_graph(
                [all_results[w][iteration][x] for x in all_results[w][iteration]],
                "CDF {} {}".format(w, iteration),
                "Latency (s)",
                "CDF",
                output_file=f"results_figures/{w}_{iteration}_cdf"
            )


main()
