#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt
import pylab
import matplotlib.lines as mlines

from utils import colors

mycolors = list(colors)
f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]

handles = [f("s", colors[i]) for i in mycolors]
labels = mycolors
#print(labels)
labels[0] = 'Algorand'
labels[1] = 'Avalanche'
labels[2] = 'Quorum'
labels[3] = 'Ethereum'
labels[4] = 'Solana'
labels[5] = 'Diem'
labels[6] = 'CollaChain'

legend = plt.legend(handles, labels, loc=1, numpoints=None, marker='-', markerscale=None, markerfirst=False, framealpha=0, frameon=False, ncol=6)


fig  = legend.figure
plt.axis('off')
fig.canvas.draw()

#plt.plot([], [], color='blue', label='Avalanche')
#plt.plot([], [], color='red', label='Solana')
#plt.plot([], [], color=colors[6], label='CollaChain')
#plt.legend(loc=0)

#bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig('legend.png') #, dpi="figure", bbox_inches=bbox)

#fig = pylab.figure()
#figlegend = pylab.figure(figsize=(3,2))
#ax = fig.add_subplot(111)
#lines = ax.plot(range(10), pylab.randn(10), range(10), pylab.randn(10))
#figlegend.legend(lines, ('one', 'two'), 'center')
#fig.show()
#figlegend.show()
#figlegend.savefig('legend.png')
