"""
Utilities and helpers for parsing the DIABLO output
Defines required classes, functions and data sets.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

colors = {}
#colors['Algorand'] = plt.cm.tab10(0)
#colors['Avalanche'] = plt.cm.tab10(1)
#colors['Libra-Diem'] = plt.cm.tab10(2)
#colors['Ethereum'] = plt.cm.tab10(3)
#colors['Quorum'] = plt.cm.tab10(4)
#colors['Solana'] = plt.cm.tab10(5)
#colors['SRBB'] = plt.cm.tab10(6)
#colors['EVM+DBFT'] = plt.cm.tab10(7)


#colors['Algorand'] = "blue"
#colors['Avalanche'] = "orange"
#colors['Libra-Diem'] = "green"
#colors['Ethereum'] = "red"
#colors['Quorum'] = "purple"
#colors['Solana'] = "brown"
#colors['SRBB'] = "pink"
#colors['EVM+DBFT'] = "grey"




#colors['Quorum-tx-propagation'] = plt.cm.tab10(0)
#colors['Quorum-no-tx-propagation'] = plt.cm.tab10(1)
#colors['Ethereum-tx-propagation'] = plt.cm.tab10(2)
#colors['Ethereum-no-tx-propagation'] = plt.cm.tab10(3)
#colors['CollaChain-3-3-4'] = plt.cm.tab10(7)

#colors['EVM+DBFT'] = plt.cm.tab10(0)
#colors['SRBB'] = plt.cm.tab10(1)

colors['SRBB'] = "blue"
#colors['20000'] = "orange"
#colors['25000'] = "green"
#colors['30000'] = "red"
#colors['35000'] = "purple"
class DiabloChainOutputResult:
    """
    An output dataset for the DIABLO output.
    """

    def __init__(self, name, data):
        """
        Initialises the Diablo Output to be easily utilised in graphing functions

        :param name - The name of the dataset
        :param all_data - All iterations for the data for a given chain
        """
        self.name = name
        self.data = data
        self.colour = colors[name]

    def add_iteration(self, iteration):
        """
        Add an iteration for the chain's benchmark run.
        :param iteration - The results of the iteration of the benchmark to add to data.
        """
        self.data.append(iteration)

    def set_colour(self, col):
        """
        Set the colour of the line for the chain
        """
        self.colour = col

def result_to_output_class(all_results: dict):
    """
    Transform the results from json to the iterations and class of output
    """

    return [DiabloChainOutputResult(ch, all_results[ch]) for ch in all_results]
