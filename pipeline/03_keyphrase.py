import argparse
import collections
import json

from tqdm import tqdm
import spacy
import pytextrank


parser = argparse.ArgumentParser()
parser.add_argument('--mode', default='abstract', choices=('title', 'abstract'))
parser.add_argument('--path', default='./data/tmp/pubmed_baseline.jsonl', type=str)
parser.add_argument('--limit', default=None, type=int)
options = parser.parse_args()


corpus = []


with open(options.path) as f:
    for line in tqdm(f, desc='read'):
        d = json.loads(line)
        if options.mode == 'title':
            corpus.append(d['title'])
        elif options.mode == 'abstract':
            corpus.append(d['abstract'])
        if options.limit is not None and len(corpus) == options.limit:
            break

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

# Read corpus and extract key phrases.
total_words = 0
vocab = collections.Counter()
for text in tqdm(corpus, desc='textrank'):
    doc = nlp(text)

    # Note: This count include punctuation as well as words.
    total_words += len(doc)

    # examine the top-ranked phrases in the document
    seen = 0
    for i, p in enumerate(doc._.phrases):
        if len(p.text.split()) == 1:
            continue
        # print("{:.3f} {}".format(p.rank, p.text))
        vocab[p.text] += 1
        seen += 1
        if seen == 10:
            break
    # print('')

for k in sorted(vocab.keys()):
    print('{} {}'.format(k, vocab[k]))
print('corpus-size={} total-words={} total-vocab={}'.format(
    len(corpus), total_words, len(vocab)))