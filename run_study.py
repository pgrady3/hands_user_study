import pickle
from open3d import visualization as o3dv
import random
import argparse
import numpy as np


def vis_judge(in_ho, out_ho, show_label=False):
    y_in, y_out = 0, 0.2
    if np.random.rand() > 0.5:
        y_in, y_out = 0.2, 0

    hand_in, obj_in = in_ho.get_o3d_meshes(hand_contact=False)
    hand_out, obj_out = out_ho.get_o3d_meshes(hand_contact=False)
    hand_in.translate((0.0, y_in, 0.0))
    obj_in.translate((0.0, y_in, 0.0))
    hand_out.translate((0.0, y_out, 0.0))
    obj_out.translate((0.0, y_out, 0.0))

    lbl_a = util.text_3d('A', pos=[-0.2, 0.0, 0], font_size=40, density=2)
    lbl_b = util.text_3d('B', pos=[-0.2, 0.2, 0], font_size=40, density=2)
    lbl_instr = util.text_3d('Press A or B', pos=[-0.2, 0.4, 0], font_size=40, density=2)

    if show_label:
        hand_in.paint_uniform_color(np.asarray([150.0, 250.0, 150.0]) / 255)  # Green
        hand_out.paint_uniform_color(np.asarray([250.0, 150.0, 150.0]) / 255)  # Red
    obj_in.paint_uniform_color(np.asarray([100.0, 100.0, 100.0]) / 255)   # Gray
    obj_out.paint_uniform_color(np.asarray([100.0, 100.0, 100.0]) / 255)  # Gray

    geom_list = [hand_in, obj_in, hand_out, obj_out, lbl_a, lbl_b, lbl_instr]

    user_result = -1    # -1 invalid, 0 liked GT, 1 liked opt

    def press_a(vis):
        nonlocal user_result
        # print('GOT A')
        if y_in == 0:
            user_result = 0
        else:
            user_result = 1
        vis.close()
        return False

    def press_b(vis):
        nonlocal user_result
        # print('GOT B')
        if y_in > 0:
            user_result = 0
        else:
            user_result = 1
        vis.close()
        return False

    key_to_callback = dict()
    key_to_callback[ord("A")] = press_a
    key_to_callback[ord("B")] = press_b
    o3dv.draw_geometries_with_key_callbacks(geom_list, key_to_callback)

    return user_result


def run_eval(args):
    in_file = 'dataset/fitted_{}.pkl'.format(args.split)
    runs = pickle.load(open(in_file, 'rb'))
    print('Loaded {} len {}'.format(in_file, len(runs)))

    print('Shuffling!!!')
    random.shuffle(runs)

    all_data = []   # Do non-parallel
    for idx, sample in enumerate(runs):
        gt_ho, in_ho, out_ho = sample['gt_ho'], sample['in_ho'], sample['out_ho']
        user_result = vis_judge(in_ho, out_ho, args.show_label)
        print('User result', user_result)
        all_data.append(user_result)

        u, u_counts = np.unique(np.array(all_data), return_counts=True)
        print(u, u_counts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run eval on fitted pkl')
    parser.add_argument('--show_label', action='store_true')
    parser.add_argument('--split', default='fine', type=str)
    args = parser.parse_args()

    run_eval(args)