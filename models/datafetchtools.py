import os 
import gzip
import tarfile
import requests

def downloadData(url, savePath):
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    print("Downloading starts")
    r = requests.get(url)
    with open(savePath, "wb") as code:
        code.write(r.content)

def extractData(tgzPath, outDir):
    os.makedirs(outDir, exist_ok=True)
    with tarfile.open(tgzPath, "r:gz") as tar:
        tar.extractall(path=outDir)       
