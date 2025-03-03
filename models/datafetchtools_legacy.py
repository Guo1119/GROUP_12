"""
datafetchtools.py - A collection of functions required for downloading and extracting zip file in the analyzer.py.

This module provides two basic tools. 

Functions:
    - downloadData(url, savePath): Download data from the given url
    - extractDat(tgzPath, outDir): Extract all content from a ".tar.gz" file


Author: Zhanshuo Guo
Version: 1.0
"""

import os 
import gzip
import tarfile
import requests

def downloadData(url: str, savePath: str):
    """
        Download a file from a url to a given path (must includes the full name of file). 
        Create a new directory if the directory in savePath doesn't exist

        Args:
            url(str): Url for downlaoding
            savePath(str): The location to be saved
    """
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    print("Downloading starts")
    r = requests.get(url)
    with open(savePath, "wb") as code:
        code.write(r.content)

def extractData(tgzPath:str, outDir:str):
    """
        Unzip a file in to a certain directory 
        Create a new directory if the directory in OutDir doesn't exist

        Args:
            tgzPath(str): Path for a ".tar.gz" file
            ouDir(str): The directory to extract all the contents inside
    """
    os.makedirs(outDir, exist_ok=True)
    with tarfile.open(tgzPath, "r:gz") as tar:
        tar.extractall(path=outDir)       
