#!/usr/bin/env python

"""
Diablo Figure Tooling
---------------------

This file contains the necessary functions to generate graphs from diablo
results.
The main purpose is to provide a simple interface to parse, then create:
    1. Figures directly from the script. (Or data ready to use)
    2. Output formatted data that can be used in tables, csvs, etc.
"""
import json
import logging
import os
import random
import sys

import click                # Library to help with command line arguments
import matplotlib.colors

import utils
import tps_time

ALL_COLOURS = list(matplotlib.colors.CSS4_COLORS)

@click.command()
@click.argument('results', default='./results')
@click.argument('output', default='./tools-output/figs/')
@click.option('--mode', required=True, type=click.Choice(['figs', 'data', 'gnuplot']))
@click.option('--base-data', required=False, help='Path to a baseline data')
@click.option('--fig', required=True, type=click.Choice(['tps', 'cdf', 'all']))
@click.option('--log-level', required=False, type=click.Choice(['INFO', 'DEBUG', 'WARNING']))
@click.option('--title', required=False, type=str)
def cli(results: str, output: str, mode: str, fig: str, base_data: str = None, log_level: str = 'INFO', title: str = None):
    """
    Run the CLI for generating the DIABLO results.

    :param results: the result directory
    :type results: str
    :param output: the output directory to store figures
    :type output: str
    :param base_data: baseline data claimed for the experiment
    :type base_data: str
    :param log_level: The logging level
    :type log_level: str
    """

    # Set the log level
    level = logging.INFO
    if log_level == 'DEBUG':
        level = logging.DEBUG
    elif log_level == 'WARNING':
        level = logging.WARNING

    logging.basicConfig(
        format='[%(levelname)s]: %(message)s',
        level=level,
    )

    logging.debug("Running with arguments: mode=%s, base=%s, fig=%s output=%s title=%s" % (mode, base_data, fig, output, title))

    # Do error checking
    if not os.path.isdir(results):
        logging.critical("Results path: \"%s\" was not found, or, is not a directory." % results)
        sys.exit(1)

    # Walk the dirs
    all_result_files = {}
    for chain in os.listdir(results):
        all_result_files[chain] = []
        for res_file in filter(lambda x: "_results.json" in x, (os.listdir(os.path.join(results, chain)))):
            logging.debug("Fetching results for %s: %s" % (chain, res_file))
            with open(os.path.join(results, chain, res_file), 'r') as f:
                all_result_files[chain].append(json.load(f))


    # Format to the results
    full_results = utils.result_to_output_class(all_result_files)

    for i in full_results:
        i.set_colour(ALL_COLOURS[sum([ord(ch) for ch in i.name]) % len(ALL_COLOURS)])

    if fig == 'all':
        # Run all figures
        logging.info("Generating all figures")
    elif fig == 'cdf':
        # Run the cdf
        logging.info("Generating CDF only")
    else:
        # Run the tx over time
        logging.info("Generating transactions over time")
        tps_time.generate_tps_graph(full_results, None, "tps over time", "seconds (s)", "throughput (tx)")


if __name__ == "__main__":
    cli()
