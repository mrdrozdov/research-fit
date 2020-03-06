import collections
import json
import os
import pubmed_parser as pp
from tqdm import tqdm


read_from = './data/raw/pubmed_baseline'
write_to = './data/tmp/pubmed_baseline.jsonl'
progress_to = './data/progress/pubmed_baseline/'


def convert_to_json(d, subkey):
    if len(d['abstract']) == 0:
        return False

    key = 'pmid_{}'.format(d['pmid'])

    check = os.path.join(progress_to, subkey, key + '.json.CHECK')
    if os.path.exists(check):
        return False

    with open(write_to, 'a') as f:
        f.write('{}\n'.format(json.dumps(d)))

    try:
        os.makedirs(os.path.dirname(check))
    except FileExistsError as e:
        pass
    with open(check, 'w') as f:
        f.write('OKOK')

    return True


abstract_counter = collections.Counter()

for i, filename in tqdm(enumerate(sorted(os.listdir(read_from)))):
    if not filename.endswith('.gz'):
        continue
    path = os.path.join(read_from, filename)
    d_lst = pp.parse_medline_xml(path)

    for d in d_lst:
        if len(d['abstract']) > 0:
            abstract_counter['has_abstract'] += 1
        abstract_counter['total'] += 1

        if convert_to_json(d, subkey='{:04}'.format(i)):
            abstract_counter['written'] += 1

    print(abstract_counter)
