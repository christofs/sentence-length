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
import os
import spacy
from spacy.lang.en import English as eng
from spacy.tokenizer import Tokenizer as tok


# === Functions


def read_metadata(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep=";", index_col=0)
    #print(metadata.head())
    return metadata


def get_metadatum(metadata, item, idno): 
    metadatum = metadata.loc[idno, item]
    return metadatum
    

def use_spacy(text, nlp, tok): 
    numtokens = len(tok(text))
    numsents = len(list(nlp(text).sents))
    return numtokens, numsents


def get_sentlen(textfile, nlp, tok): 
    """
    Calculates the average sentence length of a novel. 
    """
    with open(textfile, "r", encoding="utf8") as infile: 
        text = infile.read()
    numtokens, numsents = use_spacy(text, nlp, tok)
    avgsentlen = numtokens / numsents
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
    # Datasets
    dataset = "Gutenberg-sample3"
    # spaCy setup
    nlp = eng()
    nlp.add_pipe("sentencizer")
    nlp.max_length = 15000000
    tok = nlp.tokenizer
    # Files, folders, data container
    folder = join("..", "..", "gutenberg-samples", dataset, "texts", "PG*.txt")
    datafile = join("..", "results", dataset, "avgsentlens.csv")
    metadatafile = join("..", "corpora", dataset + "_metadata.csv")
    if not os.path.exists(join("..", "results", dataset, "")): 
        os.makedirs(join("..", "results", dataset, ""))
    data = {}
    counter = 0
    # processing
    metadata = read_metadata(metadatafile)
    for textfile in glob.glob(folder): 
        basename,ext = re.split("\.", os.path.basename(textfile))
        #print(basename)
        idno = re.split("_", basename)[0]
        year = int(get_metadatum(metadata, "year-ref", idno))
        author = get_metadatum(metadata, "shortauthor", idno)
        title = get_metadatum(metadata, "shorttitle", idno)
        print(counter, idno, year, author, title)
        avgsentlen = get_sentlen(textfile, nlp, tok)
        data[idno] = {"author" : author, "title" : title, "year" : year, "avgsentlen" : avgsentlen}
        counter +=1
    save_data(data, datafile)
        
main()
