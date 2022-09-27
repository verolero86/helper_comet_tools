#!/usr/bin/env python
# coding: utf-8
# Author: Verónica G. Melesse Vergara (@verolero86)
# Contributor: Mikaela Cashman (@mikacashman)

# This script can be used to plot histogram data produced by CoMet histogram runs

# TODO: add option to fine threshold based on number of edges and not percentages.

import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

###########################
# MAIN
###########################
if __name__ == '__main__':
    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', dest='input_file',
        help='Input histrogram file to plot')
    parser.add_argument('-t','--title', dest='title',
        default="Histogram of CoMet Data", help='Title for histogram plot')
    parser.add_argument('-m','--metric', dest='metric',
        default="DUO", help='CoMet metric (DUO/CCC/CZK)')
    parser.add_argument('-o','--output', dest='output_file',
        default="histogram", help='Prefix of output file')
    parser.add_argument('--var', dest='plot_var',
        default="LL+HH", help='Variable to plot',
        choices=['LL+HH', 'LLL+HHH', 'LL', 'HH', 'HL'])
    parser.add_argument('-c','--cutoffs',dest='user_cutoffs',
        default="1,0.1,0.01", help='Cutoff values to compute (comma seperated).')
    parser.add_argument('--verbose',dest='verbose', action="store_true",
        default=False, help='Turn on verbosity')
    args = parser.parse_args()

    # set variables for the specific run
    histfile = args.input_file
    histtitle = args.title
    metric = args.metric
    plotfile = args.output_file +".png"
    plotvar = args.plot_var

    # read histogram file
    df = pd.read_csv(histfile,delimiter="\t")
    
    # compute cutoffs
    col_sum = int(df.sum()[plotvar])
    if args.verbose: print(f"\nTotal Edges: {col_sum:,}\n")
    # note: this could be optimized
    df_cutoffs = pd.DataFrame(columns = ['Target Percentage','Actual Percentage','# Edges','Position','Score'])
    percentages = list(map(float, args.user_cutoffs.split(','))) #def=[1, 0.1, 0.01]
    for p in percentages:
        running_sum=0
        for i in range(len(df[plotvar])-1, 0, -1):
            new_sum=running_sum+df[plotvar][i]
            if(new_sum>=(p/100)*col_sum):
                final_sum=running_sum
                break;
            running_sum=new_sum
        df_cutoffs.loc[len(df_cutoffs)] = [p,(final_sum/col_sum)*100,final_sum,i,df['min'][i]]
    # printing format
    df_cutoffs.loc[:, "# Edges"] = df_cutoffs["# Edges"].map('{:,.0f}'.format)
    df_cutoffs.loc[:, "Position"] = df_cutoffs["Position"].map('{:,.0f}'.format)
    df_cutoffs.loc[:, "Actual Percentage"] = df_cutoffs["Actual Percentage"].map('{:.3f}'.format) + ' %' 
    df_cutoffs.loc[:, "Target Percentage"] = df_cutoffs["Target Percentage"].map('{:.3f}'.format) + ' %' 
    if args.verbose: print(df_cutoffs)
    if args.verbose: print("\n**Note: Scores refers to the threshold to set to include all listed edges.  \nThe actual minimum value is one notch higher.  Position refers to which line \nin the histrogram file the threshold lies at.\n")

    # plot histogram data
    ticks=[0,250,500,750,1000] #[0,1000,2000,3000,4000]
    ax=df.plot(x="min",y=plotvar,figsize=(20,10),kind='bar')
    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(ticks)
    plt.title(histtitle)
    plt.xlabel(metric+' coefficients')
    for x in range(0,len(df_cutoffs)):
        plt.axvline(x=df_cutoffs['Position'][x],color='black',label=str(percentages[x]))

    # save figure to file
    plt.savefig(plotfile)
