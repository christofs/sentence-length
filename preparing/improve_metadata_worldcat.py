# Imports

import re
import json
import pandas as pd
from os.path import join
import requests
import time
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
                


def load_metadata(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep=",", index_col=0)
        metadata = metadata
        #metadata = metadata.iloc[28:32,:] # For testing purposes
    #print(metadata.head())
    return metadata


def get_authorname(author): 
    # Get last name of author
    try: 
        author = re.sub(" \(.*?\)", "", author)
    except: 
        author = ""
        print("--No author present.")
    authorlist = re.split("\W+", author)
    stopwords = ["Le", "le", "Van", "van", "de", "De"]
    authorlist = [word for word in authorlist if word not in stopwords]
    authorlist = [word for word in authorlist if len(word) > 2]
    try: 
        authorname = authorlist[1] + "+" + authorlist[0]
    except: 
        try: 
            authorname = authorlist[0]
        except: 
            authorname = ""
    #print(authorname)
    return authorname


def get_titlewords(title): 
    # Get first content word in title
    try: 
        title = re.split("\W+", title)
    except: 
        title = ""
        print("--No title present.")
    stopwords = ["Volume"]
    title = [word for word in title if word not in stopwords]
    title = [word for word in title if len(word) > 3]
    try: 
        titlewords = title[0] +"+"+ title[1]
    except: 
        try: 
            titlewords = title[0]    
        except: 
            titlewords = ""
    #print(titlewords)
    return titlewords


def search_worldcat(authorname, titlewords): 
    querystring = str(authorname) + "+" + str(titlewords)
    url = "https://www.worldcat.org/search?q="+querystring+"&fq=&dblist=638&qt=sort&se=yr&sd=asc&qt=sort_yr_asc"
    #print(url)
    try: 
        result = requests.get(url)
        result = result.text
    except: 
        result = ""
        print("No data from worldcat.")
    time.sleep(2)
    #print(result)
    allyears = re.findall("title=\"(\d\d\d\d)\"", result)
    #print(allyears)
    try: 
        firstpubyear = min(allyears)
    except: 
        print("--No year found.")
        firstpubyear = "NA"
    #print(firstpubyear)
    return firstpubyear, url


def merge_and_save_results(metadata, results): 
    #print(metadata.head())
    #print(results.head())
    mergedmetadata = metadata.join(results, how="outer")
    print(mergedmetadata.head())
    with open(join("..", "selection", "metadata+worldcat.csv"), "w", encoding="utf8") as outfile: 
        mergedmetadata.to_csv(outfile, sep=";")
    

# === Main ===

#metadatafile = join("Gutenberg_sample1", "metadata-selected-sample.csv")
metadatafile = join("..", "selection", "metadata-fiction.csv")


def main(metadatafile): 
    metadata = load_metadata(metadatafile)
    results = {}
    counter = 0
    for item in metadata.iterrows(): 
        counter +=1
        print(counter, item[0])
        pgid = item[0]
        try: 
            author = item[1]["author"] 
        except: 
            author = ""
        authorname = get_authorname(author)
        title = item[1]["title"]
        #print(pgid, author, title)
        titlewords = get_titlewords(title)
        #print(counter, pgid, authorname, titlewords)
        firstpubyear, url = search_worldcat(authorname, titlewords)
        results[pgid] = {"firstpubyear":firstpubyear,
                         "shortauthor" : authorname,
                         "shorttitle":titlewords,
                         "worldcaturl" : url}
        #print(pgid, results[pgid])
    #print(results)
    #print(len(results))
    results = pd.DataFrame.from_dict(results, orient="index", columns=["firstpubyear",
                                                                       "shortauthor",
                                                                       "shorttitle",
                                                                       "worldcaturl"])
    merge_and_save_results(metadata, results)
        

main(metadatafile)
