import collections
import os
import pubmed_parser as pp
from tqdm import tqdm


read_from = './data/raw/pubmed_baseline'


abstract_counter = collections.Counter()

for filename in tqdm(sorted(os.listdir(read_from))):
    if not filename.endswith('.gz'):
        continue
    path = os.path.join(read_from, filename)
    d_lst = pp.parse_medline_xml(path)

    for d in d_lst:
        if len(d['abstract']) > 0:
            abstract_counter['has_abstract'] += 1
        abstract_counter['total'] += 1

    print(abstract_counter)
