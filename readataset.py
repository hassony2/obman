import argparse

from tqdm import tqdm

from obman.obman import ObMan
from obman.visutils import visualize_2d, visualize_3d

parser = argparse.ArgumentParser()
parser.add_argument('--root', required=True, help="Path to dataset root")
parser.add_argument('--shapenet_root', required=True, help="Path to root of ShapeNetCore.v2")
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
parser.add_argument('--segment', action='store_true')
parser.add_argument(
    '--mini_factor', type=float, help='Ratio in data to use (in ]0, 1[)')
parser.add_argument(
    '--root_palm', action='store_true', help='Use palm as root')
parser.add_argument('--use_cache', action='store_true', help='Use cache')
parser.add_argument('--sides', type=str, default='left')
parser.add_argument('--viz', action='store_true', help='Visualize samples')
args = parser.parse_args()

pose_dataset = ObMan(
    args.root,
    args.shapenet_root,
    split=args.split,
    use_cache=args.use_cache,
    root_palm=args.root_palm,
    mini_factor=args.mini_factor,
    mode=args.mode,
    segment=args.segment)

for i in tqdm(range(0, args.img_nb, args.img_step)):
    img_idx = args.img_idx + i
    img = pose_dataset.get_image(img_idx)
    hand_verts3d = pose_dataset.get_verts3d(img_idx)
    hand_faces = pose_dataset.get_faces3d(img_idx)
    obj_verts3d, obj_faces = pose_dataset.get_obj_verts_faces(img_idx)
    hand_joints2d = pose_dataset.get_joints2d(img_idx)
    hand_verts2d = pose_dataset.get_verts2d(img_idx)
    hand_joints2d = pose_dataset.get_joints2d(img_idx)
    obj_verts2d = pose_dataset.get_obj_verts2d(img_idx)

    if args.viz:
        visualize_2d(
            img,
            hand_joints=hand_joints2d,
            hand_verts=hand_verts2d,
            obj_verts=obj_verts2d)
        visualize_3d(
            img,
            hand_verts=hand_verts3d,
            hand_faces=hand_faces,
            obj_verts=obj_verts3d,
            obj_faces=obj_faces)
