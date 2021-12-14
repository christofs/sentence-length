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
import matplotlib.pyplot as plt
import pygal
from pygal.style import BlueStyle
from pygal.style import Style
import seaborn as sns
from os.path import join
import os

# === Functions

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
    boundaries = root.findall(".//tei:body//tei:w[@n='SENT']", ns)
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
    dataset = "ELTeC-eng_level2"
    folder = join(dataset, "data", "ENG*.xml")
    datafile = join(dataset, "results", "avgsentlens.csv")
    data = {}
    for xmlfile in glob.glob(folder): 
        basename,ext = re.split("\.", os.path.basename(xmlfile))
        idno = re.split("_", basename)[0]
        year = re.findall("\d\d\d\d", basename)[0]
        author = re.split("_", basename)[1]
        avgsentlen = get_sentlen(xmlfile)
        data[idno] = {"author" : author, "year" : year, "avgsentlen" : avgsentlen}
    save_data(data, datafile)
        
main()
