#!/usr/bin/env python3
"""
For first generatig a frequency list from the given file
"""
from getqed import getqd
import os
from konlpy.tag import Okt
from collections import defaultdict
import csv
from argparse import ArgumentParser

def make_frequency(filename : str, limit:int=1000):
    parser = Okt()
    if not os.path.isdir(filename):
        raise FileNotFoundError
    print("Making frequency dictionary")
    dictionary = defaultdict(lambda : 0)
    count = 0 # Use for tracking messages
    for sentence in getqd(filename):
        morphs = parser.morphs(sentence, norm=True, stem=True)
        for m in morphs:
            dictionary[m] += 1
        count += 1
        notify_interval = 10000
        if count % notify_interval == 0:
            print(f"Processed {count} sentences...")
        if limit and count > limit:
            break
    return dictionary

def write_dictionary(dictionary, outfile):
    vals = sorted(list(dictionary.items()), key = lambda x : x[1], reverse=True)
    with open(outfile, "w") as f:
        writer = csv.writer(f)
        for r in vals:
            writer.writerow(list(r))

def read_dictionary(infile : str):
    # We could make the list here as well but we dont to make things simpler
    dict = {} # for fast look up
    with open(infile, "r") as f:
        r = csv.reader(f)
        for word, count in r:
            dict[word] = int(count)
    return dict

if __name__ == "__main__":
    # d = make_frequency("./data/QED/xml/ko", 10000)
    # write_dictionary(d, "test.csv")
    # print(read_dictionary("test.csv"))
    parser = ArgumentParser()
    parser.add_argument("--directory", default="./data/QED/raw/ko")
    parser.add_argument("--limit", default=10000, type=int)
    parser.add_argument("--outfile", default="dictionary.csv")

    args = parser.parse_args()
    d = make_frequency(args.directory, args.limit)
    write_dictionary(d, args.outfile)
