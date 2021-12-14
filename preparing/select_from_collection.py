
# === Imports

import pandas as pd 
import numpy as np
import os
from os.path import join
import shutil


# === Functions

def read_metadata(): 
    metadatafile = join("..", "metadata", "metadata.csv")
    with open(metadatafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=",", index_col=0)
    #print(data.head())
    return data
    


def filter_metadata(data): 
    # select only fiction
    data["sentlenset"] = data['subjects'].apply(lambda x: True if "fiction" in x.lower() else False)
    data = data[(data["sentlenset"] == True)]
    # exclude sound
    data = data[(data["type"] != "Sound")]
    # select only English
    data = data[(data["language"] == "['en']")]
    # select only texts between specific author birth and death
    #data["birth"] = pd.to_numeric(data["authoryearofbirth"])
    #data["death"] = pd.to_numeric(data["authoryearofdeath"])
    #data = data[(data["birth"] >= 1700) & (data["death"] <= 1980)]
    # define "purported year of publication" (pyearp)
    #data["ageatdeath"] = data["death"] - data["birth"]
    #data["pyearp"] = round(data["death"] - data["ageatdeath"]/2)
    # select only texts from range of pyearp
    #data = data[(data["pyearp"] >=1750) & (data["pyearp"] <=1950)]
    # clean up
    data = data.drop(["sentlenset"], axis=1)

    print(data.head())
    print(data.shape)
    return data


def create_sample(data):
    """
    Selects a random sample of relevant texts from the selected data.
    """
    datasample = data.sample(n=320)
    return datasample


def save_metadata(data, filename):
    with open(join("..", "metadata", filename), "w", encoding="utf8") as outfile: 
        data.to_csv(outfile) 
        


def copy_subset(datasample): 
    selids = list(datasample.index)
    destdir = join("..", "selection", "sample3", "text", "")
    if not os.path.exists(destdir): 
        os.makedirs(destdir)
    selfns = [join("..", "data", "text", selid + "_text.txt") for selid in selids]
    print(len(selfns))
    #print(selfns)
    for selfn in selfns: 
        if os.path.isfile(selfn):
            shutil.copy(selfn, destdir)
            


# === Main

def main(): 
    data = read_metadata()
    data = filter_metadata(data)
    save_metadata(data, join("..", "selection", "metadata-fiction.csv"))
    #datasample = create_sample(data)
    #save_metadata(datasample, join("..", "selection", "metadata-selected-sample3.csv"))
    #copy_subset(datasample)

main()
