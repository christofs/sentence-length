"""
Script to establish the average sentence length per novel, and over time, 
in the English corpus of the European Literary Text Collection (ELTeC-eng). 
"""

# === Imports

import re
import pandas as pd
import glob
from os.path import join
import xml.etree.ElementTree as ET
import os

# === Functions


def read_metadata(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep="\t", index_col=0)
    print(metadata.head())
    return metadata


def get_sentlen(xmlfile): 
    """
    Calculates the average sentence length of a novel. 
    Does not calculate the length of each sentence separately. 
    Based on the level-2 encoding of ELTeC. 
    Simply counts the total number of tokens and divides this number
    by the total number of sentence boundary punctuation.     
    """
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    root = ET.parse(xmlfile).getroot()
    tokens = root.findall(".//tei:body//tei:w", ns)
    boundaries = root.findall(".//tei:body//tei:s", ns)
    avgsentlen = len(tokens) / len(boundaries)
    return avgsentlen
                
  
def save_data(data, datafile): 
    """
    Saves the sentence length data to a CSV file / table. 
    """
    data = pd.DataFrame(data).T
    #print(data.head())
    with open(datafile, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep=";")


# === Main

def main(): 
    """
    Coordinates the process. 
    """
    # Files, folders, data containers
    dataset = "ELTeC-hun_level2"
    #dataset = "ELTeC-deu_level2"
    textfolder = join("..", "data", dataset, "texts", "HU*.xml")
    sentlenfile = join("..", "results", dataset, "avgsentlens.csv")
    metadatafile = join("..", "data", dataset, "metadata.csv")
    if not os.path.exists(join("..", "results", dataset, "")): 
        os.makedirs(join("..", "results", dataset, ""))
    data = {}
    metadata = read_metadata(metadatafile)
    for xmlfile in glob.glob(textfolder): 
        #print(xmlfile)
        idno,ext = re.split("\.", os.path.basename(xmlfile))
        author = metadata.loc[idno, "au-name"]
        year = metadata.loc[idno,"firsted-yr"]
        avgsentlen = get_sentlen(xmlfile)
        print(idno, author, year, avgsentlen)
        data[idno] = {"author" : author, "year" : year, "avgsentlen" : avgsentlen}
    save_data(data, sentlenfile)
        
main()
