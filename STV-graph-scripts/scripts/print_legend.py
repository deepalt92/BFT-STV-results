#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

from utils import colors

# use LaTeX to manage layout
plt.rcParams['text.usetex'] = 'true'
plt.rcParams.update({'font.size': 30})
# override fonts
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = 'Palatino'

mycolors = list(colors)
labels = sns.color_palette('Dark2', n_colors=8, desat=0.8)        
palette=sns.blend_palette(colors=labels, n_colors=8, input='rgb')
f = lambda m,c: plt.plot([],[],marker=" ", color=c, ls="-")[0]
handles = [f("s", colors[i]) for i in mycolors]
#mycolors = list(palette)
#labels = mycolors
#print(labels)
labels[0] = 'Algorand'
labels[1] = 'Avalanche'
labels[2] = 'Libra-Diem'
labels[3] = 'Ethereum'
labels[4] = 'Quorum'
labels[5] = 'Solana'
labels[6] = 'SRBB'
labels[7] = 'EVM+DBFT'
#labels[0] = 'Quorum'
#labels[1] = 'Quorum-TPR'
#labels[2] = 'Ethereum'
#labels[3] = 'Ethereum-TPR'

#labels[0] = 'EVM+DBFT'
#labels[1] = 'SRBB'

#labels[0] = '15000'
#labels[1] = '20000'
#labels[2] = '25000'
#labels[3] = '30000'
#labels[4] = '35000'

legend = plt.legend(handles, labels, loc=0, framealpha=1, frameon=False, ncol=8)

def export_legend(legend, filename="newlegend.pdf"):
    fig  = legend.figure
    plt.axis('off')
    # fix problem due to matplotlib version
    #fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig.draw(renderer=renderer)
    ###
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox, format='pdf')

export_legend(legend)
