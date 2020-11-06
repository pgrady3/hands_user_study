import numpy as np
from open3d import io as o3dio
from open3d import geometry as o3dg
from open3d import utility as o3du
from open3d import visualization as o3dv
from PIL import Image, ImageFont, ImageDraw
from pyquaternion import Quaternion


def text_3d(text, pos, direction=None, degree=-90.0, density=10, font='FreeMono.ttf', font_size=10):
    if direction is None:
        direction = (0., 0., 1.)

    font_obj = ImageFont.truetype(font, font_size * density)
    font_dim = font_obj.getsize(text)

    img = Image.new('RGB', font_dim, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font_obj, fill=(0, 0, 0))
    img = np.asarray(img)
    img_mask = img[:, :, 0] < 128
    indices = np.indices([*img.shape[0:2], 1])[:, img_mask, 0].reshape(3, -1).T

    pcd = o3dg.PointCloud()
    pcd.colors = o3du.Vector3dVector(img[img_mask, :].astype(float) / 255.0)
    # pcd.points = o3d.utility.Vector3dVector(indices / 100.0)
    pcd.points = o3du.Vector3dVector(indices / 1000 / density)

    raxis = np.cross([0.0, 0.0, 1.0], direction)
    if np.linalg.norm(raxis) < 1e-6:
        raxis = (0.0, 0.0, 1.0)
    trans = (Quaternion(axis=raxis, radians=np.arccos(direction[2])) *
             Quaternion(axis=direction, degrees=degree)).transformation_matrix
    trans[0:3, 3] = np.asarray(pos)
    pcd.transform(trans)
    return pcd


def get_meshes(hand_verts, hand_faces, obj_verts, obj_faces):
    hand_color = np.asarray([224.0, 172.0, 105.0]) / 255
    obj_color = np.asarray([100.0, 100.0, 100.0]) / 255

    hand_mesh = o3dg.TriangleMesh()
    hand_mesh.vertices = o3du.Vector3dVector(hand_verts)
    hand_mesh.triangles = o3du.Vector3iVector(hand_faces)
    hand_mesh.compute_vertex_normals()
    hand_mesh.paint_uniform_color(hand_color)

    obj_mesh = o3dg.TriangleMesh()
    obj_mesh.vertices = o3du.Vector3dVector(obj_verts)
    obj_mesh.triangles = o3du.Vector3iVector(obj_faces)
    obj_mesh.compute_vertex_normals()
    obj_mesh.paint_uniform_color(obj_color)

    return hand_mesh, obj_mesh