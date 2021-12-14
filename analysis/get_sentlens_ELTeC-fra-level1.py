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
import spacy
from spacy.lang.en import English as eng
from spacy.lang.fr import French as fra
from spacy.tokenizer import Tokenizer as tok
import os

# === Functions


def read_metadata(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep="\t", index_col=0)
    #print(metadata.head(2))
    return metadata

def use_spacy(para, nlp, tok): 
    numtokens = len(tok(para))
    numsents = len(list(nlp(para).sents))
    return numtokens, numsents


def get_sentlen(xmlfile, nlp, tok): 
    """
    Calculates the average sentence length of a novel. 
    Does not calculate the length of each sentence separately. 
    Based on the level-2 encoding of ELTeC. 
    Simply counts the total number of tokens and divides this number
    by the total number of sentence boundary punctuation.     
    """
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    root = ET.parse(xmlfile).getroot()
    paras = root.findall(".//tei:body//tei:p", ns)
    #print(len(paras))
    allnumtokens = 0
    allnumsents = 0
    for para in paras: 
        paratext = "".join(para.itertext())
        paratext = re.sub(" {1,50}", " ", paratext)
        paratext = re.sub("\t{1,10}", " ", paratext)
        paratext = re.sub("\n{1,3}", " ", paratext)
        paratext = re.sub(" {1,50}", " ", paratext)
        #print(paratext)
        numtokens, numsents = use_spacy(paratext, nlp, tok)
        allnumtokens += numtokens
        allnumsents += numsents
    avgsentlen = allnumtokens / allnumsents
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
    dataset = "ELTeC-fra_level1"
    textfolder = join("..", "data", dataset, "texts", "FRA*.xml")
    sentlenfile = join("..", "results", dataset, "avgsentlens.csv")
    metadatafile = join("..", "data", dataset, "metadata.csv")
    language = "fra"
    if not os.path.exists(join("..", "results", dataset, "")): 
        os.makedirs(join("..", "results", dataset, ""))
    data = {}
    # spaCy setup
    if language == "eng": 
        nlp = eng()
    elif language == "fra": 
        nlp = fra()
    nlp.add_pipe("sentencizer")
    tok = nlp.tokenizer
    metadata = read_metadata(metadatafile)
    for xmlfile in glob.glob(textfolder): 
        #print(xmlfile)
        basename,ext = re.split("\.", os.path.basename(xmlfile))
        idno = re.split("_", basename)[0]
        author = re.split("_", basename)[1]
        year = metadata.loc[basename,"firsted-yr"]
        avgsentlen = get_sentlen(xmlfile, nlp, tok)
        print(idno, author, year, avgsentlen)
        data[idno] = {"author" : author, "year" : year, "avgsentlen" : avgsentlen}
    save_data(data, sentlenfile)
        
main()
