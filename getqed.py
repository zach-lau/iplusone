"""
Code to extract files from QED database
"""
import os
import xml.etree.ElementTree as ET
import random

random.seed(8)

def getqd(dirname : str):
    if not os.path.isdir(dirname):
        raise FileNotFoundError 
    def extract(file : str):
        """ Extract from the given file"""
        t = ET.parse(file)
        r = t.getroot()
        for elem in r.findall('s'):
            # yield ' '.join([x.text for x in elem.findall('w')]) # Reconstruct from parsed
            for text in elem.itertext():
                text = text.strip()
                if len(text) > 0:
                    yield text
    files = os.listdir(dirname)
    random.shuffle(files)

    for file in files:
        file = os.path.join(dirname, file)
        try:
            yield from extract(file)
        except Exception as e:
            print(f"Problem with file {file}", e)
            continue

if __name__ == "__main__":
    gen = getqd("./data/test")
    for _ in range(3):
        print(next(gen))
    
    