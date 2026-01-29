import os
import requests
import zipfile

base = "CMP_facade_DB_base.zip"
extended = "CMP_facade_DB_extended.zip"

for dataset in (base, extended):
    resp = requests.get(f"https://cmp.felk.cvut.cz/~tylecr1/facade/{dataset}")
    with open(dataset, "wb") as f:
        f.write(resp.content)
    with zipfile.ZipFile(dataset, "r") as f:
        f.extractall(".")
    os.remove(dataset)
    os.remove("label_names.txt")
    os.remove("readme.txt")

os.rename("base", "b")
os.rename("extended", "x")
