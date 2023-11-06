"""
Code to extract files from QED database
"""
import os
import xml.etree.ElementTree as ET

def getqd(dirname : str):
    if not os.path.isdir(dirname):
        raise FileNotFoundError 
    def extract(file : str):
        """ Extract from the given file"""
        t = ET.parse(file)
        r = t.getroot()
        for elem in r.iter('s'):
            # This construction is kind if ugly with punctuation but hopefully our tokenize handles it
            yield ' '.join([x.text for x in elem.findall('w')])

    for file in os.listdir(os.path.join(dirname)):
        file = os.path.join(dirname, file)
        try:
            yield from extract(file)
        except Exception as e:
            print(f"Problem with file {file}", e)
            continue

if __name__ == "__main__":
    print(next(getqd("./data/QED/xml/ko")))
    