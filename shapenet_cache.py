import csv
import os
import pickle
import traceback

import numpy as np
import trimesh
from tqdm import tqdm
from joblib import Parallel, delayed

from obman.loadutils import fast_load_obj

selected_csv = 'assets/shapenet_select.csv'
shapenet_info = {}
with open(selected_csv, 'r') as csv_f:
    reader = csv.DictReader(csv_f)
    for row_idx, row in enumerate(reader):
        shapenet_info[row['class']] = row['path']

for class_id, class_path in tqdm(shapenet_info.items(), desc='class'):
    samples = sorted(os.listdir(class_path))
    for sample in tqdm(samples, desc='sample'):
        sample_path = os.path.join(class_path, sample,
                                   'models/model_normalized.obj')
        if (class_id == '02958343') and (sample == '207e69af994efa9330714334794526d4'):
            continue
        else:
            try:
                with open(sample_path, 'r') as obj_f:
                    mesh = fast_load_obj(obj_f)
                    assert len(mesh) == 1
                    mesh_dict = {
                        'vertices': mesh[0]['vertices'],
                        'faces': mesh[0]['faces'],
                    }
                    mesh = trimesh.load(mesh_dict)
                save_path = sample_path.replace('.obj', '.pkl')
                mesh_dict = {
                    'vertices': np.array(mesh.vertices).astype(np.float32),
                    'faces': np.array(mesh.faces)
                }
                with open(save_path, 'wb') as p_f:
                    pickle.dump(mesh_dict, p_f)
            except Exception:
                traceback.print_exc()
                print(class_id, sample)
