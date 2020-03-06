import argparse
import collections
import json
from multiprocess import Pool

from tqdm import tqdm
import spacy
import pytextrank


parser = argparse.ArgumentParser()
parser.add_argument('--mode', default='abstract', choices=('title', 'abstract'))
parser.add_argument('--path', default='./data/tmp/pubmed_baseline.jsonl', type=str)
parser.add_argument('--maxdocs', default=None, type=int)
parser.add_argument('--maxphrases_per_doc', default=10, type=int)
parser.add_argument('--nproc', default=4, type=int)
options = parser.parse_args()


corpus = []


with open(options.path) as f:
    for line in tqdm(f, desc='read'):
        d = json.loads(line)
        if options.mode == 'title':
            corpus.append(d['title'])
        elif options.mode == 'abstract':
            corpus.append(d['abstract'])
        if options.maxdocs is not None and len(corpus) == options.maxdocs:
            break

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

# Read corpus and extract key phrases.
def worker(text):
    doc = nlp(text)
    phrases = [p.text for p in doc._.phrases]
    num_words = len(doc)
    return phrases, num_words

p = Pool(options.nproc)
total_words = 0
vocab = collections.Counter()
for phrases, num_words in tqdm(p.imap(worker, corpus)):
    # Note: This count include punctuation as well as words.
    total_words += num_words

    # examine the top-ranked phrases in the document
    seen = 0
    for i, p in enumerate(phrases):
        if len(p.split()) == 1:
            continue
        # print("{:.3f} {}".format(p.rank, p.text))
        vocab[p] += 1
        seen += 1
        if options.maxphrases_per_doc > 0 and seen == options.maxphrases_per_doc:
            break

for k in sorted(vocab.keys()):
    print('{} {}'.format(k, vocab[k]))
print('corpus-size={} total-words={} total-vocab={}'.format(
    len(corpus), total_words, len(vocab)))