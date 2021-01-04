import subprocess
import os
import sys

import numpy as np
import pickle
from svgpathtools import svg2paths

def print_progress(text, i, max_i):
    """Print Progress."""
    sys.stdout.write('\r' + text + str(i) + ' / ' + str(max_i))
    sys.stdout.flush()
    if i == max_i:
        print('')

# Raw svg data need to have viewbox=0 0 1000 1000 and width=height=26.45834 then use:
# (-t can specify the linesimplification, heigher means more simplification)
def simplify(load_svg_path, save_svg_path, linesimplify=0.1, round_decimals=1):
    subprocess.run(f'vpype read {load_svg_path} linemerge linesimplify -t {linesimplify} write temp.svg', shell=True)
    if not os.path.isfile("temp.svg"):
        return
    svg_polylines_string = []
    for path in svg2paths("temp.svg")[0]:
        line = np.array([[p.end.real, p.end.imag] for p in path]).flatten().round(round_decimals)
        svg_polylines_string.append("".join(['<polyline points="', " ".join(line.astype(str)), '"/>']))
    os.remove("temp.svg")

    if len(svg_polylines_string) == 0:
        return
    
    svg_string_prefex = '<svg xmlns="http://www.w3.org/2000/svg" height="26.45834cm" viewBox="0 0 1000 1000" width="26.45834cm">\n<g fill="none" stroke="#00f">'
    svg_polylines_string = "\n".join(svg_polylines_string)
    svg_string_suffex = '</g>\n</svg>'
    svg_string = "\n".join([svg_string_prefex, svg_polylines_string, svg_string_suffex])
    with open(save_svg_path, 'w') as f:
        f.write(svg_string)

def simplify_dir(load_dir, save_dir, linesimplify=0.1, round_decimals=1):
    os.mkdir(save_dir)
    for i, fn in enumerate(os.listdir(load_dir)):
        print_progress("simplify svg ", i+1, len(os.listdir(load_dir)))
        load_svg_path = os.path.join(load_dir, fn)
        save_svg_path = os.path.join(save_dir, fn)
        simplify(load_svg_path, save_svg_path, linesimplify, round_decimals)

def save_simplified_svg_dir_with_pickle(load_dir, save_path):
    dataset = []
    for i, fn in enumerate(os.listdir(load_dir)):
        print_progress("read svg ", i+1, len(os.listdir(load_dir)))
        load_svg_path = os.path.join(load_dir, fn)
        lines = []
        for path in svg2paths(load_svg_path)[0]:
            lines.append(np.array([[p.end.real, p.end.imag] for p in path], dtype=np.float16).flatten())
        dataset.append(lines)

    with open(save_path, 'wb') as f:
        pickle.dump(dataset, f)
