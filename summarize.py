import pickle
import random
import argparse
import numpy as np
import bz2
from util import *
import json
import time


# READ_FILES = ['results_fine_gerry.json']
# READ_FILES = ['results_fine_gerry.json', 'results_fine_me.json']
# READ_FILES = ['results_im_ani.json', 'results_im_me.json']
# READ_FILES = ['results_im_ani.json']
# READ_FILES = ['results_fine_bog.json']    # Used a different split
# READ_FILES = ['results_fine_me_nosmall_2.json']
READ_FILES = ['results_im_me_nosmall.json']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run study')
    parser.add_argument('--show_label', action='store_true')
    parser.add_argument('--split', default='fine', type=str)
    args = parser.parse_args()

    all_dicts = []
    for file_path in READ_FILES:
        with open(file_path) as f:
            data = json.load(f)
        all_dicts.extend(data)

    all_stats = {}
    for key in all_dicts[0].keys():
        all_stats[key] = list()
        for d in all_dicts:
            all_stats[key].append(d[key])

    for obj in set(all_stats['obj_name']):
        this_obj = []
        for d in all_dicts:
            if obj == d['obj_name']:
                this_obj.append(d['result'])
        print('Object {:.2f} {}'.format(np.array(this_obj).mean(), obj))

    print('Mean score', np.array(all_stats['result']).mean())
    print('Mean time', np.array(all_stats['elapsed']).mean())


    p = np.array(all_stats[key]).mean()
    p0 = 0.5

    z = (p - p0) / np.sqrt(p * p * (1/75 + 1/75))
    print(z)
    print('length', len(all_stats['result']))
