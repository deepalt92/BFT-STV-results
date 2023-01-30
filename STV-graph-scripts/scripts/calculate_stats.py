#!/usr/bin/env python

import itertools
import json
import yaml
import os
import sys

import utils
import numpy as np

# WORKLOADS = ["community", "company", "elitist", "toy"]
WORKLOADS = ["amazon", "apple", "dota2000", "facebook", "football", "gafam", "google", "microsoft", "uber", "youtube"]

if (len(sys.argv) < 2):
    print("[INVALID base dir] -- usage: python rough_figures.py /path/to/results/dir")
    print("Example: python figs/rough_figures.py /home/testuser/Diablo/results/")
    sys.exit(1)

base = sys.argv[1].strip()

all_results = {w: {} for w in WORKLOADS}

# Iterate through workload (community, company ..)
for workload in WORKLOADS:
    workload_number = list(filter(lambda x: '.DS_Store' not in x, os.listdir(os.path.join(base, workload))))
    all_results[workload] = {wn: {} for wn in workload_number}


    # Get the workload number (100, 1000, 100000....)
    for wn in workload_number:
        # Find the result directory
        for res_dir in filter(lambda x: ".tar.gz" not in x and '.DS_Store' not in x, os.listdir(os.path.join(base, workload, wn))):

            # Filter out non-result files
            for filename in filter(lambda x: "_results.json" in x, os.listdir(os.path.join(base, workload, wn, res_dir))):

                # First step, read the name of the chain
                current_name = ""
                with open(os.path.join(base, workload, wn, res_dir, "name.txt"), 'r') as f:
                    current_name = ''.join(f.readlines()).strip()

                # Then read the data
                data = None
                with open(os.path.join(base, workload, wn, res_dir, filename), 'r') as f:
                    data = json.load(f)

                # spec = None
                # spec_path = os.path.join(base, workload, wn, res_dir, filename.replace('_results.json', '_workload.yaml'))
                # if os.path.exists(spec_path):
                #     with open(spec_path, 'r') as f:
                #         spec = yaml.safe_load(f)
                #     assert(str(spec['bench']['txs'][0]) == wn)

                if current_name not in all_results[workload][wn]:
                    all_results[workload][wn][current_name] = utils.DiabloChainOutputResult(name=current_name, data=[data])
                else:
                    all_results[workload][wn][current_name].add_iteration(data)

                # Add the data back to that chain for that workload

# output = {}
# for c in ['quorum-ibft', 'poa', 'solana', 'diem', 'avalanche']:
#     output[c] = {}
#     for i in ['100', '1000', '10000']:
#         output[c][i] = {}
#         for v in ['company', 'toy', 'elitist', 'community']:
#             output[c][i][v] = ' &  & '

for w in all_results:
    for iteration in all_results[w]:
        for chain in all_results[w][iteration]:
            if chain != 'algorand':
                continue
            for run, data in enumerate(all_results[w][iteration][chain].data):
                avg_throughput = -1
                peak_throughput = -1
                avg_latency = -1
                throughputs = []
                throughputs_orig_len = 0
                latencies = []
                if data['SecondaryResults'] is not None:
                    secondary_throughputs = map(lambda l: l['ThroughputSeconds'], data['SecondaryResults'])
                    zipped_throughputs = zip(*secondary_throughputs)
                    throughputs = list(map(sum, zipped_throughputs))
                    throughputs_orig_len = len(throughputs)
                    # throughputs = throughputs[:121]
                    if len(throughputs) > 0:
                        avg_throughput = np.average(throughputs)
                        peak_throughput = np.max(throughputs)
                    secondary_latencies = map(lambda l: l['TxLatencies'], data['SecondaryResults'])
                    chained_latencies = itertools.chain.from_iterable(secondary_latencies)
                    latencies = list(filter(lambda x: x > 0, chained_latencies))
                    if len(latencies) > 0:
                        avg_latency = np.average(latencies)/1000
                    # if avg_throughput > 0 and avg_latency > 0:
                    #     output[chain][iteration][w] = str(peak_throughput) + ' & ' + ('{:.1f}' if avg_throughput < 10 else '{:.0f}').format(avg_throughput) + ' & ' + ('{:.1f}' if avg_latency < 10 else '{:.0f}').format(avg_latency)
                print('topology:{} workload:{} chain:{} run:{} len:{} throughputs:{} avg:{:.1f} {:.0f} peak:{} latencies:{} avg:{:.1f} {:.0f}'.format(w, iteration, chain, run, throughputs_orig_len, len(throughputs), avg_throughput, avg_throughput, peak_throughput, len(latencies), avg_latency, avg_latency))
                # print(str(peak_throughput) + ' & ' + ('{:.1f}' if avg_throughput < 10 else '{:.0f}').format(avg_throughput) + ' & ' + ('{:.1f}' if avg_latency < 10 else '{:.0f}').format(avg_latency))
                print()

# for c in ['quorum-ibft', 'poa', 'solana', 'diem', 'avalanche']:
#     for i in ['100', '1000', '10000']:
#         print(' &  &  & ' + ' & '.join([output[c][i][v] for v in ['company', 'toy', 'elitist', 'community']]) + ' & {} \\\\'.format(i))


# current_data = all_results['10000']['1']['solana'].data[0]
# # total_throughput = current_data['TotalThroughputOverTime']
# # print(len(total_throughput))
# print(np.average(current_data['TotalThroughputOverTime'][:123]))
# # print(np.sum(current_data['AverageThroughputSecondaries']))
# duration = 300
# print(list(map(lambda l: len(l[:duration]), current_data['TotalThrouhgputPerSecondaryPerWindow'])))
# print(np.sum(list(map(lambda l: np.average(l[:duration]), current_data['TotalThrouhgputPerSecondaryPerWindow']))))
# print(np.sum(list(map(lambda l: np.max(l[:duration]), current_data['TotalThrouhgputPerSecondaryPerWindow']))))
# print(np.sum(list(map(lambda l: np.average(l['ThroughputSeconds'][:duration]), current_data['SecondaryResults']))))
# print(np.sum(list(map(lambda l: np.max(l['ThroughputSeconds'][:duration]), current_data['SecondaryResults']))))

# print(np.max(list(map(sum, zip(*current_data['TotalThrouhgputPerSecondaryPerWindow'])))))
# print(np.average(list(map(sum, zip(*current_data['TotalThrouhgputPerSecondaryPerWindow'])))))

# print(current_data.keys())
# print(current_data['SecondaryResults'][0].keys())
# print()
