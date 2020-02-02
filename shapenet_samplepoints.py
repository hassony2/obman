import argparse
import csv
import os
import pickle
import traceback

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
from tqdm import tqdm
from scipy.spatial import Delaunay

from obman.loadutils import fast_load_obj
from obman.samplemesh import sample_mesh, points_from_mesh


def create_ray_samples(sample_path,
                       min_hits=2000,
                       volumic=False,
                       display=False):
    try:
        if os.path.exists(sample_path):
            with open(sample_path, 'rb') as obj_f:
                mesh_dict = pickle.load(obj_f)
        else:
            with open(sample_path.replace('.pkl', '.obj'), 'r') as obj_f:
                mesh_dict = fast_load_obj(obj_f)[0]
        print('Loaded {}'.format(sample_path))

        mesh = trimesh.load(mesh_dict)
        tri = Delaunay(mesh_dict['vertices'])
        if display:
            dmesh = Poly3DCollection(
                mesh_dict['vertices'][tri.simplices[:, :3]], alpha=0.5)
            dmesh.set_edgecolor('b')
            dmesh.set_facecolor('r')
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(121, projection='3d')
            ax.add_collection3d(dmesh)
        if volumic:
            points = trimesh.sample.volume_mesh(mesh, count=min_hits)
            save_path = '/' + os.path.join(*sample_path.split('/')[:-1],
                                           'volume_points.pkl')
        else:
            points = sample_mesh(mesh, min_hits=min_hits)
            if display:
                ax = fig.add_subplot(122, projection='3d')
                ax.scatter(points[:, 0], points[:, 1], points[:, 2])
                plt.show()
            save_path = '/' + os.path.join(*sample_path.split('/')[:-1],
                                           'surface_points.pkl')
        with open(save_path, 'wb') as p_f:
            pickle.dump(points, p_f)
    except Exception:
        traceback.print_exc()
        if not volumic:
            obj_faces = np.array(mesh.faces)
            obj_verts3d = np.array(mesh.vertices)
            points = points_from_mesh(
                obj_faces, obj_verts3d, show_cloud=False, vertex_nb=min_hits)
            save_path = '/' + os.path.join(*sample_path.split('/')[:-1],
                                           'surface_points.pkl')
            print('Post_processing', save_path)
            with open(save_path, 'wb') as p_f:
                pickle.dump(points, p_f)
            print(class_id, sample)
    print('Saved {}'.format(save_path))


if __name__ == "__main__":
    # selected_csv = '/sequoia/data2/dataset/shapenet/selected_atlas.csv'
    parser = argparse.ArgumentParser()
    parser.add_argument('--group_by', default=4000, type=int)
    parser.add_argument('--start_idx', default=0, type=int)
    args = parser.parse_args()
    selected_csv = 'assets/shapenet_select.csv'
    shapenet_info = {}
    with open(selected_csv, 'r') as csv_f:
        reader = csv.DictReader(csv_f)
        for row_idx, row in enumerate(reader):
            shapenet_info[row['class']] = row['path']

    sample_paths = []
    for class_id, class_path in tqdm(shapenet_info.items(), desc='class'):
        samples = sorted(os.listdir(class_path))
        for sample in tqdm(samples, desc='sample'):
            sample_path = os.path.join(class_path, sample,
                                       'models/model_normalized.pkl')

            if class_id == '02958343' and (
                    sample == '207e69af994efa9330714334794526d4'):
                continue
            else:
                sample_paths.append(sample_path)

    print('Handling {} to {} from {} samples'.format(
        args.start_idx, args.start_idx + args.group_by, len(sample_paths)))
    for sample in tqdm(
            sample_paths[args.start_idx:args.start_idx + args.group_by]):
        create_ray_samples(sample)
