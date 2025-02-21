import os 
import gzip
import tarfile
import requests

def downloadData(url, savePath):
    print("Downloading starts")
    r = requests.get(url)
    with open(savePath, "wb") as code:
        code.write(r.content)

def extractData(tgzPath, outDir):
    os.makedirs(outDir, exist_ok=True)
    with tarfile.open(tgzPath, "r:gz") as tar:
        tar.extractall(path=outDir)       
