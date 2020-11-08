import pickle
import random
import argparse
import numpy as np
import bz2
from util import *
import json
import time


READ_FILES = ['results_gerry.json']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run study')
    parser.add_argument('--show_label', action='store_true')
    parser.add_argument('--split', default='fine', type=str)
    args = parser.parse_args()

    all_dicts = []
    for file_path in READ_FILES:
        with open(file_path) as f:
            data = json.load(f)
        all_dicts.append(data)

    all_stats = {}
    for key in ['elapsed', 'result']:
        all_stats[key] = list()
        for d in all_dicts:
            for el in d:
                all_stats[key].append(el[key])

    for key in all_stats:
        print(key, all_stats[key])
        print(key, np.array(all_stats[key]).mean())

    p = np.array(all_stats[key]).mean()
    p0 = 0.5

    z = (p - p0) / np.sqrt(p * p * (1/75 + 1/75))
    print(z)
