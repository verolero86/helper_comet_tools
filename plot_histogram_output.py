#!/usr/bin/env python
# coding: utf-8
# Author: Verónica G. Melesse Vergara (@verolero86)

# This script can be used to plot histogram data produced by CoMet histogram runs

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# set variables for the specific run
# TODO: make these arguments
histfile = "/path/to/histogram/file/histogram_2way_123456.txt"
histtitle = "Histogram for Some Data"
metric = "DUO"
plotfile = "2way_histogram.png"
plotvar = "LL+HH" # for 3-way: "LLL+HHH"

# read histogram file
df = pd.read_csv(histfile,delimiter="\t")

# plot histogram data
ticks=[0,1000,2000,3000,4000]
ax=df.plot(x="min",y=plotvar,figsize=(20,10),kind='bar')
ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(ticks)
plt.title(histtitle)
plt.xlabel(metric+' coefficients')

# save figure to file
plt.savefig(plotfile)
