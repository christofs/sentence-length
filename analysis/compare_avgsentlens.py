"""
Script to visualize the average sentence length per novel, and over time.
"""

# === Imports

import re
import pandas as pd
import glob
from os.path import join
import matplotlib.pyplot as plt
import os
import seaborn as sns
import random
import numpy as np


# === Functions

def read_data(datafile): 
    """
    Reads the CSV file with the average sentence length per text, plus metadata.
    """
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";", index_col=0)
    print(data.head())
    return data



def filter_data(data, comparison, samplesize): 
    """
    Selects the average sentence length values for all texts that fall 
    into the two periods specified by the comparison parameter. 
    Returns two Series with values for each of the two periods. 
    """
    # First series of data
    vals1 = data[(data["year"] >= comparison[0][0]) & (data["year"] <= comparison[0][1])]
    vals1 = list(vals1.loc[:,"avgsentlen"])
    print("vals1", len(vals1))
    vals1 = random.sample(vals1, samplesize)
    med1 = np.median(vals1)
    vals1 = pd.Series(vals1, name=str(comparison[0][0]) + "–" + str(comparison[0][1])+"\n(median="+'{0:.2f}'.format(med1)+")")
    # Second series of data
    vals2 = data[(data["year"] >= comparison[1][0]) & (data["year"] <= comparison[1][1])]
    vals2 = list(vals2.loc[:,"avgsentlen"])   
    print("vals2", len(vals2))
    vals2 = random.sample(vals2, samplesize)
    med2 = np.median(vals2)
    vals2 = pd.Series(vals2, name=str(comparison[1][0]) + "–" + str(comparison[1][1])+"\n(median="+'{0:.2f}'.format(med2)+")")
    return vals1, vals2, med1, med2


def plot_seaborn(comparison, vals1, vals2, med1, med2, filename, samplesize, p): 
    # Labels
    title="Comparison of average sentence length distributions"
    xlabel="Average sentence length\n(samplesize="+str(samplesize)+", p="+'{0:.10f}'.format(p)+")"
    ylabel="Density (KDE)"
    plot = sns.displot([vals1, vals2], kind="kde", fill=True, rug=True)
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title)
    #regplot = sns.regplot(x="year", y="avgsentlen", marker=".", data=data, x_jitter=0.3, order=3, color="#117b99", scatter_kws={"color": "#117b99"}, line_kws={"color": "#00264D"}).set_title("Average sentence length per novel in " + dataset)
    #fig = plot.get_figure()
    #plt.grid()
    plot.savefig(filename, dpi=600)
    


def test_significance(vals1, vals2): 
    """
    Perform a significance test for the difference between the two distributions.
    At the moment, based only on the sample selected above, not on the full data.
    """
    from scipy.stats import mannwhitneyu
    stat, p = mannwhitneyu(vals1, vals2)
    return stat, p




# === Main

def main(): 
    """
    Coordinates the process. 
    """
    # Parameters
    dataset = "Gutenberg-sample3"
    comparison = [(1840,1859), (1900,1919)]
    samplesize = 250
    # Files, folders, data container
    datafile = join("..", "results", dataset, "avgsentlens.csv")
    filename_dists = join("..", "results", dataset, "comparison_"+str(comparison[0][0]) + "-" + str(comparison[0][1])+"-vs-"+str(comparison[1][0]) + "-" + str(comparison[1][1])+".png")
    # Functions
    data = read_data(datafile)
    vals1,vals2,med1,med2 = filter_data(data, comparison, samplesize)
    stat,p = test_significance(vals1, vals2)
    plot_seaborn(comparison, vals1, vals2, med1, med2, filename_dists, samplesize, p)
    print("\nDone comparing values in", dataset)
        
main()
