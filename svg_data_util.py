import os
import sys

import numpy as np
import pickle
from svgpathtools import svg2paths
import pandas as pd
from rdp import rdp

def svg_to_lines(svg_path):
    lines = []
    for path in svg2paths(svg_path)[0]:
        lines.append(np.array([[p.end.real, p.end.imag] for p in path], dtype=np.float16).flatten())
    return lines

def simplify_lines(lines, max_xy=1000, rdp_epsilon=1):
    new_lines = []
    for line in lines:
        line = np.array(line)
        if rdp_epsilon is not None:
            line = line.reshape(-1, 2)
            line = rdp(line.tolist(), epsilon=rdp_epsilon)
            line = np.array(line).flatten()
        new_lines.append(np.round(line/1000*max_xy))
    return new_lines

def get_svg_from_lines(lines, max_xy=1000, background="#e9e9e9"):
    if background is not None:
        background_str = f'<rect x="-100" y="-100" width="1100" height="1100" fill="{background}" />'
    else:
        background_str = ''
    polyline_strs = [''.join(['<polyline fill=\"none\" stroke=\"#00f\" points=\"', ' '.join((np.array(line)*1000/max_xy).astype(str)), '\"/>']) for line in lines]
    svg_str = '\n'.join(['<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"26.45834cm\" viewBox=\"0 0 1000 1000\" width=\"26.45834cm\">', background_str] + polyline_strs + ['</svg>'])
    return svg_str

def save_svg(save_path, svg):
    with open(save_path, 'w') as f:
        f.write(svg)

def print_progress(text, i, max_i):
    """Print Progress."""
    sys.stdout.write('\r' + text + str(i) + ' / ' + str(max_i))
    sys.stdout.flush()
    if i == max_i:
        print('')

def svg_dir_to_dataset_pkl(load_dir, save_path):
    dataset = []
    for i, fn in enumerate(sorted(os.listdir(load_dir))):
        print_progress("read svg ", i+1, len(os.listdir(load_dir)))
        dataset.append(svg_to_lines(os.path.join(load_dir, fn)))

    with open(save_path, 'wb') as f:
        pickle.dump(dataset, f)

def dataset_pkl_to_lines(load_dataset_path):
    return pd.read_pickle(load_dataset_path)

def save_simplified_dataset_pkl(load_dataset_path, save_dataset_path, svg_count_in_new_dataset=None, max_xy=1000, rdp_epsilon=1):
    svg_lines = dataset_pkl_to_lines(load_dataset_path)
    new_svg_lines = []
    if svg_count_in_new_dataset is None:
        svg_count_in_new_dataset = len(svg_lines)
    else:
        svg_count_in_new_dataset = min(svg_count_in_new_dataset, len(svg_lines))

    for i, svg in enumerate(svg_lines[:svg_count_in_new_dataset]):
        print_progress("process svg ", i+1, svg_count_in_new_dataset)
        new_svg_lines.append(simplify_lines(svg, max_xy, rdp_epsilon))
    
    with open(save_dataset_path, 'wb') as f:
        pickle.dump(new_svg_lines, f)




