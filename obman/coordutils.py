import numpy as np


def get_coords_2d(coords3d, cam_extr=None, cam_calib=None):
    if cam_extr is None:
        coords2d_hom = np.dot(cam_calib, coords3d.transpose())
    else:
        coords3d_hom = np.concatenate(
            [coords3d, np.ones((coords3d.shape[0], 1))], 1)
        coords3d_hom = coords3d_hom.transpose()
        coords2d_hom = np.dot(cam_calib, np.dot(cam_extr, coords3d_hom))
    coords2d = coords2d_hom / coords2d_hom[2, :]
    coords2d = coords2d[:2, :]
    return coords2d.transpose()
