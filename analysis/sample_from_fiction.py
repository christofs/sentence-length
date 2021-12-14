
# === Imports

import pandas as pd 
import numpy as np
import os
from os.path import join
import shutil


# === Functions

def read_metadata(fictionmetadatafilename): 
    with open(fictionmetadatafilename, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";", index_col=0)
    print(data.head())
    return data
    


def filter_metadata(data, timeframe): 
    # select only texts between specific publication dates
    data = data[(data["year-ref"] >= timeframe[0]) & (data["year-ref"] <= timeframe[1])]
    # clean up
    #print(data.head())
    #print(data.shape)
    return data



def create_sample(data, samplesize):
    """
    Selects a random sample of relevant texts from the selected data.
    """
    datasample = data.sample(n=samplesize)
    #print(type(datasample))
    return datasample



def sliced_sampling(data, timeframe, samplesize):
    subsamplesize = int(np.round(samplesize / (timeframe[1]-timeframe[0]) * 10))
    subtimeframes = []
    start = timeframe[0]
    while start < timeframe[1]-9: 
        subtimeframes.append([start,start+9])
        start +=10
    #print(subsamplesize)
    #print(timeframes_by_decade)
    print("sample:", len(subtimeframes), "decades;", subsamplesize, "texts per decade;", len(subtimeframes*subsamplesize), "texts in total.")
    slicedsample = pd.DataFrame()
    for subtimeframe in subtimeframes: 
        subdata = filter_metadata(data, subtimeframe)
        subsample = create_sample(subdata, subsamplesize)
        slicedsample = slicedsample.append(subsample)
    #print(slicedsample)
    return slicedsample
    

def save_metadata(data, samplemetadatafilename):
    with open(join(samplemetadatafilename), "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep=";") 
        

def copy_subset(datasample, origdir, destdir): 
    selids = list(datasample.index)
    selfns = [join(origdir, selid + "_text.txt") for selid in selids]
    #print(len(selfns))
    #print(selfns)
    copied = 0
    missing = 0
    for selfn in selfns: 
        if os.path.isfile(selfn):
            shutil.copy(selfn, destdir)
            copied +=1
        else: 
            missing +=1
    print("Copied", copied, "files. Missing:", missing, "files.")
            


# === Main

def main(): 
    # Parameters
    fictionmetadatafilename = join("..", "..", "gutenberg-fiction", "metadata-fiction+worldcat+heuristics+fixes.csv")
    dataset = "Gutenberg-sample3"
    origdir = join("..", "..", "gutenberg-fiction", "text", "")
    destdir = join("..", "..", "gutenberg-samples", dataset, "texts", "")
    samplemetadatafilename = join("..", "corpora", dataset +"_metadata.csv")
    samplesize = 4200
    timeframe = [1820,1940]
    sampletype = "overall" # "overall"|"decades"
    if not os.path.exists(destdir): 
        os.makedirs(destdir)
    # Create sample
    data = read_metadata(fictionmetadatafilename)
    if sampletype == "overall": 
        data = filter_metadata(data, timeframe)
        datasample = create_sample(data, samplesize)
    elif sampletype == "decades": 
        datasample = sliced_sampling(data, timeframe, samplesize)        
    save_metadata(datasample, samplemetadatafilename)
    copy_subset(datasample, origdir, destdir)

main()
