import pickle
import random
import argparse
import numpy as np
import bz2
from util import *
import json
from open3d import io as o3dio
from open3d import geometry as o3dg
from open3d import utility as o3du
from open3d import visualization as o3dv


def run_samples(fine_samples, args):
    for idx in range(3):
        sample = fine_samples[idx]
        hand_in, obj_in = get_meshes(sample['hand_verts_in'], sample['hand_faces'], sample['obj_verts'], sample['obj_faces'])
        hand_out, obj_out = get_meshes(sample['hand_verts_out'], sample['hand_faces'], sample['obj_verts'], sample['obj_faces'])
        hand_out.translate((0.0, 0.2, 0.0))
        obj_out.translate((0.0, 0.2, 0.0))

        if idx == 0:
            hand_in.translate((0.05, 0, 0.01))
            lbl_a = text_3d('A', pos=[-0.2, 0.0, 0], font_size=40, density=2)
            lbl_b = text_3d('B', pos=[-0.2, 0.2, 0], font_size=40, density=2)
        elif idx == 1:
            hand_out.translate((0, 0.01, -0.05))
            lbl_a = text_3d('A', pos=[-0.2, 0.2, 0], font_size=40, density=2)
            lbl_b = text_3d('B', pos=[-0.2, 0.0, 0], font_size=40, density=2)
        elif idx == 2:
            hand_out.translate((0, 0.02, 0))
            lbl_a = text_3d('A', pos=[-0.2, 0.0, 0], font_size=40, density=2)
            lbl_b = text_3d('B', pos=[-0.2, 0.2, 0], font_size=40, density=2)

        lbl_instr_1 = text_3d('Practice example {}. Select the more'.format(idx + 1), pos=[-0.25, 0.33, 0], font_size=25, density=2)
        lbl_instr_2 = text_3d('natural looking grasp. Press A or B', pos=[-0.25, 0.30, 0], font_size=25, density=2)

        geom_list = [hand_in, obj_in, hand_out, obj_out, lbl_a, lbl_b, lbl_instr_1, lbl_instr_2]

        def press_a(vis):
            vis.close()

        def press_b(vis):
            vis.close()

        key_to_callback = {ord("A"): press_a, ord("B"): press_b}
        o3dv.draw_geometries_with_key_callbacks(geom_list, key_to_callback)


    text_list = ['End of practice samples.',
                 ' ',
                 'Press Q to proceed to the study.']

    geom_list = []
    for idx, t in enumerate(text_list):
        geom_list.append(text_3d(t, pos=[0, -0.04 * idx, 0], font_size=40, density=2))

    o3dv.draw_geometries(geom_list, zoom=0.45, front=[0, 0, 1], lookat=[0.3, -0.05, 0], up=[0, 1, 0])


def run_intro(args):
    text_list = ['Thank you for participating in the study.',
                 'You will be shown two hand/object pairs',
                 'and asked to choose which one looks more natural.',
                 'Please press the indicated key to choose.',
                 ' ',
                 'The view perspective can be shifted by:',
                 'Clicking and dragging to rotate',
                 'Scrolling to zoom, and Ctrl+clicking to pan',
                 'You can practice here.',
                 ' ',
                 'Press Q to proceed to practice examples']

    geom_list = []
    for idx, t in enumerate(text_list):
        geom_list.append(text_3d(t, pos=[0, -0.04 * idx, 0], font_size=40, density=2))

    o3dv.draw_geometries(geom_list, zoom=0.45, front=[0, 0, 1], lookat=[0.6, -0.2, 0], up=[0, 1, 0])


def run_sample(sample, args):
    hand_in, obj_in = get_meshes(sample['hand_verts_in'], sample['hand_faces'], sample['obj_verts'], sample['obj_faces'])
    hand_out, obj_out = get_meshes(sample['hand_verts_out'], sample['hand_faces'], sample['obj_verts'], sample['obj_faces'])

    out_is_top = np.random.rand() > 0.5
    a_is_top = np.random.rand() > 0.5

    hand_in.translate((0.0, int(not out_is_top) * 0.2, 0.0))
    obj_in.translate((0.0, int(not out_is_top) * 0.2, 0.0))
    hand_out.translate((0.0, int(out_is_top) * 0.2, 0.0))
    obj_out.translate((0.0, int(out_is_top) * 0.2, 0.0))

    lbl_a = text_3d('A', pos=[-0.2, int(a_is_top) * 0.2, 0], font_size=40, density=2)
    lbl_b = text_3d('B', pos=[-0.2, int(not a_is_top) * 0.2, 0], font_size=40, density=2)
    lbl_instr_1 = text_3d('Select the more natural looking grasp.', pos=[-0.25, 0.33, 0], font_size=25, density=2)
    lbl_instr_2 = text_3d('Press A or B', pos=[-0.25, 0.30, 0], font_size=25, density=2)

    if args.show_label:
        hand_in.paint_uniform_color(np.asarray([150.0, 250.0, 150.0]) / 255)  # Green
        hand_out.paint_uniform_color(np.asarray([250.0, 150.0, 150.0]) / 255)  # Red

    geom_list = [hand_in, obj_in, hand_out, obj_out, lbl_a, lbl_b, lbl_instr_1, lbl_instr_2]

    user_result = -1    # -1 invalid, 0 liked GT, 1 liked opt

    def press_a(vis):
        nonlocal user_result
        user_result = int(out_is_top == a_is_top)
        vis.close()

    def press_b(vis):
        nonlocal user_result
        user_result = int(out_is_top != a_is_top)
        vis.close()

    key_to_callback = {ord("A"): press_a, ord("B"): press_b}
    o3dv.draw_geometries_with_key_callbacks(geom_list, key_to_callback)

    return user_result


def run_study(args):
    in_file = 'study.pkl'
    runs = pickle.load(bz2.BZ2File(in_file, 'rb'))
    print('Loaded database file: {}'.format(in_file, len(runs)))

    run_intro(args)
    run_samples(runs['fine'], args)

    results = list()
    splits = runs.keys()
    for idx, split in enumerate(splits):
        split_samples = runs[split]
        random.shuffle(split_samples)
        print('Randomizing order')

        for sample in split_samples:
            out = dict()
            out['hash'] = sample['hash']
            out['split'] = split
            out['obj_name'] = sample['obj_name']
            out['result'] = run_sample(sample, args)
            results.append(out)

            with open('result.json', 'w') as fp:
                json.dump(results, fp, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run study')
    parser.add_argument('--show_label', action='store_true')
    args = parser.parse_args()

    run_study(args)
