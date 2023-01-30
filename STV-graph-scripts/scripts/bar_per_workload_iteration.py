"""
Workload Iteration Comparison

Bar plot comparing throughput, fails, etc.
"""

import pandas as pd
import seaborn as sns

def generate_barplot(dataset, title, x_label, y_label, baseline=None, output_file=None):
    """
    Generates the barplot
    """

    formatted_data = []

    for chain in dataset:
        print(chain.name)