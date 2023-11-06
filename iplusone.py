#!/usr/bin/env python3
"""
iplusone sentence generator
"""

from getqed import getqd
from freqlist import read_dictionary
import os
from konlpy.tag import Okt
from math import log
import csv
from argparse import ArgumentParser
import heapq

class ExampleEntry:
    def __init__(self, word, rank):
        self.word = word
        self.rank = rank
        self.examples = []
        self.size = 3
    def add_example(self, new_example : str, score : float):
        """ Compare to the current example and replace it if better"""
        heapq.heappush(self.examples, (score, new_example))
        if len(self.examples) > self.size:
            heapq.heappop(self.examples)

class Worker():
    def __init__(self, dict_file : str, data_dir : str):
        # Setup
        self.examples = None
        if not os.path.isfile(dict_file):
            raise FileNotFoundError
        if not os.path.isdir(data_dir):
            raise FileNotFoundError
        self.parser = Okt()
        self.data_dir = data_dir
        # Read data
        self.counts = read_dictionary(dict_file)
        self.total_words = sum(self.counts.values())
        print(f"Got {self.total_words} total words")
        # flist = sorted(counts.keys(), key=lambda x : counts[x]) # sorted version of all the words
        self.flist = sorted(self.counts.keys(), key=lambda x: self.counts[x], reverse=True)
        self.total_unique_words = len(self.flist)
        print(f"Got {self.total_unique_words} unique words")

    # Helper functions
    def get_hardest_index(self, morphs : list):
        hi = 0
        hc = self.counts[morphs[0]]
        for index, m in enumerate(morphs):
            if self.counts[m] < hc:
                hi = index
                hc = self.counts[m]
        return hi

    def get_sentence_score(self, target_index : int, morphs : list):
        # Won't hanlde having the same morpheme twice but oh well
        def get_information(count : int, total:int = self.total_words):
            return -log(count)+log(self.total_words)
        local_counts = [self.counts[m] for m in morphs]
        local_info = [get_information(c) for c in local_counts]
        target_info = local_info[target_index]
        total_info = sum(local_info)
        fraction_info = target_info/total_info
        # Function to translate from fraction to score
        def f(x):
            # beta distribution
            a = 1
            b = 5
            return x**a*(1-x)**b
        return f(fraction_info)

    def make_i_plus_one(self, limit:int=10000):
        # Create i+1 sentences
        self.examples = {}
        for rank, word in enumerate(self.flist):
            self.examples[word] = ExampleEntry(word, rank)
        count = 0 # To check against limit
        for sentence in getqd(self.data_dir):
            morphs = self.parser.morphs(sentence)
            # Check valid sentence
            if len(morphs) == 0:
                continue
            def contains_all_morphs(list, morphs):
                for m in morphs:
                    if not m in list:
                        return False
                return True
            if not contains_all_morphs(self.counts, morphs):
                continue
            hardest_index = self.get_hardest_index(morphs)
            hardest_morph = morphs[hardest_index] 
            score = self.get_sentence_score(target_index = hardest_index, morphs=morphs)
            target_entry = self.examples[hardest_morph]
            target_entry.add_example(sentence, score)
            count += 1
            interval = 10000
            if count % interval == 0:
                print(f"Processed {count} sentences...")
            if limit and count > limit:
                break
        return self.examples

    def write_examples(self, outfile : str):
        with open(outfile, "w") as f:
            writer = csv.writer(f)
            for entry in sorted(self.examples.values(), key=lambda x : x.rank):
                examples = [x[1] for x in entry.examples[::-1]]
                writer.writerow([entry.rank, entry.word, *examples])
    
    # Test functinos
    def parse(self, sentence):
        """ Get morphs from a sentence """
        return self.parser.morphs(sentence)
    def get_counts(self, morphs):
        """ Get counts for a list of morphs """
        return [self.counts[m] for m in morphs]

if __name__ == '__main__':
    # w = Worker('test.csv', 'data/QED/xml/ko')
    # w.make_i_plus_one(limit=10000)
    # w.write_examples("test_ex.csv")
    parser = ArgumentParser()
    parser.add_argument("--dictionary", default="dictionary.csv")
    parser.add_argument("--data", default="./data/QED/xml/ko")
    parser.add_argument("--limit", default=10000, type=int)
    parser.add_argument("--outfile", default="examples.csv")
    args = parser.parse_args()
    w = Worker(args.dictionary, args.data)
    w.make_i_plus_one(limit=args.limit)
    w.write_examples(args.outfile)
