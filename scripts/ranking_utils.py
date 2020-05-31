from typing import List
from random import shuffle
from argparse import ArgumentParser
import csv
from pathlib import Path


def split_files(files: List[str], n: int, dataset: str):
    data = []
    for filename in files:
        with open(filename, 'r') as tsvin:
            filedata = csv.reader(tsvin, delimiter='\t')
            for row in filedata:
                data.append(row)
    split_size = len(data) // n
    shuffle(data)
    print('Split sizes: {}'.format(split_size))
    groups = []
    for i in range(n):
        start = i*split_size
        if i != n-1:
            groups.append(data[start:start+split_size])
        else:
            groups.append(data[start:])
    base_path = 'data/stacked/{}'.format(dataset)
    for i in range(n):
        Path('{}/split_{}'.format(base_path, i)).mkdir(parents=True, exist_ok=True)
        train = []
        val = groups[i]
        for j in range(n):
            if i != j:
                train.extend(groups[j])
        with open('{}/split_{}/train.tsv'.format(base_path, i), 'w') as file:
            writer = csv.writer(file, delimiter='\t', lineterminator='\n')
            writer.writerows(train)
        with open('{}/split_{}/val.tsv'.format(base_path, i), 'w') as file:
            writer = csv.writer(file, delimiter='\t', lineterminator='\n')
            writer.writerows(val)
    print('Done...')

if __name__ == '__main__':
    ap = ArgumentParser(description='Argument parsing for NPP paper dataset creartion')
    ap.add_argument('-s', '--src-files', nargs='+', type=str, help='Source file -- if given, system output ' +
                    'should be a set of N TSVs', required=True,
                    default=None)
    ap.add_argument('-N', '--num', type=int, help='How manay splits to create', default=5)
    ap.add_argument('-d', '--dataset',choices=['e2e', 'weather', 'weather_challenge'], required=True)
    args = ap.parse_args()
    split_files(args.src_files, args.num, args.dataset)
    