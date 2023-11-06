# Iplusone
This is a program for createing iplusone sentences from a corpus with application to Korean using QED

# Datasets
Data sets for the sample sentences are taken from the QCRI Educational Domain Corpus [1] as distributed by OPUS [2].
They are not available as part of this repository and can be downloaded from https://opus.nlpl.eu/QED-v2.0a.php

# NLP
Morpheme analysis uses the Okt NLP program from https://github.com/open-korean-text/open-korean-text [3] available
through the konlpy python package [4]

# Usage
There are two tools
- `freqlist.py`: constructs a frequency list from the corpus. Outputs to `dictionary.csv`
- `iplusone.py`: create i-plus-one sentences ordered by the frequency list using sentences from the given corpus.
  Outputs to `example.csv`

By default both programs will stop after processing 10 000 sentences. To avoid this limit use --limit 0

To modify for use with other corpuses replace the `getqed` function with an appropriate generator based on the corpus
structure.

# Examples
Example outputs can be found in the sample-outputs directory

# Algorithm
## `freqlist.py`
Frequency list generation is straight-forward.

## `iplusone.py`
iplusone generation proceeds as follows:

For each sentence
- Identify the hardest morpheme
- Evaluate the suitability of this sentence as an example for this target word.
    - At the time of writing this is done based on the fraction of shannon information in the target morpheme with a
      beta(1,5) function for the suitability. The ideal sentence would have 1/6 of the information in the target
morpheme.
- Each morpheme keeps a heap of its best morphemes ordered based on score. The new sentence will be inserted into this
  heap. Once all sentences are processed we are done.

Runtime for both tools is linear in the number of sentences and will take a few seconds per 10 000 sentences.

# License
The QED corpus is subject to the license in `LICENSE.qed` and covers the example sentences found in the example outputs.
These are available for research usage only. The remainder of the code is subject to the Apache license.

# References
[1] A. Abdelali, F. Guzman, H. Sajjad and S. Vogel, "The AMARA Corpus: Building parallel language resources for the
educational domain", The Proceedings of the 9th International Conference on Language Resources and Evaluation (LREC'14).
Reykjavik, Iceland, 2014. Pp. 1856-1862. Isbn. 978-2-9517408-8-4. 

[2] OPUS for distributing the corpus: J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of
the 8th International Conference on Language Resources and Evaluation

[3] H. Ryu. "open-korean-text", Github repository, https://github.com/open-korean-text/open-korean-text

[4] Eunjeong L. Park, Sungzoon Cho. “KoNLPy: Korean natural language processing in Python”, Proceedings of the 26th
Annual Conference on Human & Cognitive Language Technology, Chuncheon, Korea, Oct 2014.
