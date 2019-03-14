import argparse
from collections import defaultdict
import os
import pickle

from matplotlib import pyplot as plt
import numpy as np
from PIL import ImageStat
import scipy.misc
from tqdm import tqdm
import torch

from obman import ObMan

parser = argparse.ArgumentParser()
parser.add_argument(
    '--split', type=str, default='train', help='Usually [train|test]')
parser.add_argument(
    '--mode',
    default='all',
    choices=['all', 'obj', 'hand'],
    help='Mode for synthgrasp dataset')
parser.add_argument(
    '--img_idx', type=int, default='1', help='Idx of first image to display')
parser.add_argument(
    '--img_nb', type=int, default='10', help='Number of images to display')
parser.add_argument(
    '--img_step', type=int, default='1', help='Number of images to display')
parser.add_argument(
    '--joint_idxs', action='store_true', help='Display joint indexes')
parser.add_argument('--segment', action='store_true')
parser.add_argument(
    '--mini_factor', type=float, help='Ratio in data to use (in ]0, 1[)')
parser.add_argument(
    '--root_palm', action='store_true', help='Use palm as root')
parser.add_argument('--use_cache', action='store_true', help='Use cache')
parser.add_argument('--center_idx', type=int, default=0)
parser.add_argument('--sides', type=str, default='left')
parser.add_argument('--viz', action='store_true', help='Visualize samples')
args = parser.parse_args()

pose_dataset = ObMan(
    split=args.split,
    use_cache=args.use_cache,
    root_palm=args.root_palm,
    version=args.version,
    mini_factor=args.mini_factor,
    mode=args.mode,
    segment=args.segment)
