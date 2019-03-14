from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from obman import viz2d


def visualize_2d(img,
                 hand_joints=None,
                 hand_verts=None,
                 obj_verts=None,
                 links=[(0, 1, 2, 3, 4), (0, 5, 6, 7, 8), (0, 9, 10, 11, 12),
                        (0, 13, 14, 15, 16), (0, 17, 18, 19, 20)]):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(img)
    ax.axis('off')
    if hand_joints is not None:
        viz2d.visualize_joints_2d(
            ax, hand_joints, joint_idxs=False, links=links)
    if obj_verts is not None:
        ax.scatter(obj_verts[:, 0], obj_verts[:, 1], alpha=0.1, c='r')
    if hand_verts is not None:
        ax.scatter(hand_verts[:, 0], hand_verts[:, 1], alpha=0.1, c='b')
    plt.show()


def visualize_3d(img,
                 hand_verts=None,
                 hand_faces=None,
                 obj_verts=None,
                 obj_faces=None):
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.imshow(img)
    ax.axis('off')
    ax = fig.add_subplot(122, projection='3d')
    add_mesh(ax, hand_verts, hand_faces)
    add_mesh(ax, obj_verts, obj_faces, c='r')
    cam_equal_aspect_3d(ax, hand_verts)
    plt.show()


def add_mesh(ax, verts, faces, alpha=0.1, c='b'):
    mesh = Poly3DCollection(verts[faces], alpha=alpha)
    if c == 'b':
        face_color = (141 / 255, 184 / 255, 226 / 255)
    elif c == 'r':
        face_color = (226 / 255, 184 / 255, 141 / 255)
    edge_color = (50 / 255, 50 / 255, 50 / 255)
    mesh.set_edgecolor(edge_color)
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)


def cam_equal_aspect_3d(ax, verts, flip_x=False):
    """
    Centers view on cuboid containing hand and flips y and z axis
    and fixes azimuth
    """
    extents = np.stack([verts.min(0), verts.max(0)], axis=1)
    sz = extents[:, 1] - extents[:, 0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    if flip_x:
        ax.set_xlim(centers[0] + r, centers[0] - r)
    else:
        ax.set_xlim(centers[0] - r, centers[0] + r)
    # Invert y and z axis
    ax.set_ylim(centers[1] + r, centers[1] - r)
    ax.set_zlim(centers[2] + r, centers[2] - r)
