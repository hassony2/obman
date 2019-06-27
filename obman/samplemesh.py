from matplotlib import pyplot as plt
import numpy as np
import trimesh
from obman.loadutils import fast_load_obj


def spherical_to_vector(spherical):
    """
    Copied from trimesh great library !
    see https://github.com/mikedh/trimesh/blob/4c9ab1e9906acaece421f
    b189437c8f4947a9c5a/trimesh/util.py
    Convert a set of (n,2) spherical vectors to (n,3) vectors
    Parameters
    -----------
    spherical : (n , 2) float
       Angles, in radians
    Returns
    -----------
    vectors : (n, 3) float
      Unit vectors
    """
    spherical = np.asanyarray(spherical, dtype=np.float64)

    theta, phi = spherical.T
    st, ct = np.sin(theta), np.cos(theta)
    sp, cp = np.sin(phi), np.cos(phi)
    vectors = np.column_stack((ct * sp, st * sp, cp))
    return vectors


def sample_surface_sphere(count, center=np.array([0, 0, 0]), radius=1):
    """
    Copied from trimesh great library !
    see https://github.com/mikedh/trimesh/blob/4c9ab1e9906acaece421f
    b189437c8f4947a9c5a/trimesh/util.py
    Correctly pick random points on the surface of a unit sphere
    Uses this method:
    http://mathworld.wolfram.com/SpherePointPicking.html
    Parameters
    ----------
    count: int, number of points to return
    Returns
    ----------
    points: (count,3) float, list of random points on a unit sphere
    """

    u, v = np.random.random((2, count))

    theta = np.pi * 2 * u
    phi = np.arccos((2 * v) - 1)

    points = center + radius * spherical_to_vector(
        np.column_stack((theta, phi)))
    return points


def sample_mesh(mesh, min_hits=2000, ray_nb=3000, interrupt=10):
    verts = np.array(mesh.vertices)
    centroid = verts.mean(0)
    radius = max(np.linalg.norm(verts - centroid, axis=1))
    # print('radius ', radius)
    origins = sample_surface_sphere(ray_nb, centroid, radius=2 * radius)
    hits = None
    counts = 0
    while hits is None or hits.shape[0] < min_hits:
        counts += 1
        destination = centroid + sample_surface_sphere(ray_nb, radius=radius)
        directions = destination - (origins)
        # print('Casting rays ! ')
        locations, index_ray, index_tri = mesh.ray.intersects_location(
            ray_origins=origins,
            ray_directions=directions,
            multiple_hits=False)
        # print('Got {} hits'.format(locations.shape))
        if hits is None:
            hits = locations
        else:
            hits = np.concatenate([hits, locations])
        if counts > interrupt:
            raise Exception('Exceeded {} attempts'.format(interrupt))
    return hits
    # return hits, centroid, destination


def tri_area(v):
    return 0.5 * np.linalg.norm(
        np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]), axis=1)


def points_from_mesh(faces, vertices, vertex_nb=600, show_cloud=False):
    """
    Points are sampled on the surface of the mesh, with probability
    proportional to face area
    """
    areas = tri_area(vertices[faces])

    proba = areas / areas.sum()
    rand_idxs = np.random.choice(
        range(areas.shape[0]), size=vertex_nb, p=proba)

    # Randomly pick points on triangles
    u = np.random.rand(vertex_nb, 1)
    v = np.random.rand(vertex_nb, 1)

    # Force bernouilli couple to be picked on a half square
    out = u + v > 1
    u[out] = 1 - u[out]
    v[out] = 1 - v[out]

    rand_tris = vertices[faces[rand_idxs]]
    points = rand_tris[:, 0] + u * (rand_tris[:, 1] - rand_tris[:, 0]) + v * (
        rand_tris[:, 2] - rand_tris[:, 0])

    if show_cloud:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(
            points[:, 0],
            points[:, 1],
            points[:, 2],
            s=2,
            c='b')
        ax.scatter(
            vertices[:, 0],
            vertices[:, 1],
            vertices[:, 2],
            s=2,
            c='r')
        ax._axis3don = False
        plt.show()
    return points
if __name__ == "__main__":
    model_path = ('/sequoia/data2/yhasson/datasets/'
                  'modelnet_meshes_2018_10_02/glass_000001702_12.obj')
    model_path = ('/sequoia/data2/yhasson/datasets/'
                  'modelnet_meshes_2018_10_02/bottle_000001910_21.obj')

    # with open(model_path, 'rb') as obj_f:
    #     mesh_dict = pickle.load(obj_f)
    with open(model_path, 'r') as obj_f:
        mesh_dict = fast_load_obj(obj_f)[0]
        mesh = trimesh.load(mesh_dict)

    # hits, centroid, origins = sample_mesh(mesh)
    hits = sample_mesh(mesh)
    fig = plt.figure()
    ax = fig.add_subplot(122, projection='3d')
    ax.scatter(hits[:, 0], hits[:, 1], hits[:, 2], alpha=0.1)
    # ax.scatter(origins[:, 0], origins[:, 1], origins[:, 2], alpha=0.1)
    # ax.scatter(centroid[0], centroid[1], centroid[2], alpha=1, c='r')
    plt.show()
