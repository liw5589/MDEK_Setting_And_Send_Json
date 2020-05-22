import pyrealsense2 as rs
import math
import numpy as np
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Depth image filter
spatial = rs.spatial_filter()
spatial.set_option(rs.option.holes_fill, 3)
hole_filling = rs.hole_filling_filter()
depth_to_disparity = rs.disparity_transform(True)
disparity_to_depth = rs.disparity_transform(False)

def disparity():
    def func(x, a, b):
        return a * x ** 2 + b  # Quadratic function

    h, w = CAMERA_HEIGHT // 2, CAMERA_WIDTH
    result_image = np.zeros((h, w, 3)).astype('uint8')
    for i in range(h):
        result_image[CAMERA_HEIGHT // 2 - 1 - i] = int(func(i, fit_log[0], fit_log[1]))

    return result_image

def depth_filter(depth_data):
    depth_data = depth_to_disparity.process(depth_data)
    depth_data = spatial.process(depth_data)
    depth_data = disparity_to_depth.process(depth_data)
    depth_data = hole_filling.process(depth_data)
    return depth_data

def pixel_to_3d(pixel_x, pixel_y, depth_image, depth_intrinsics):  # Convert pixel (x, y), depth to (x, y, z) coord
    coord = [pixel_y, pixel_x]
    z, x, y = rs.rs2_deproject_pixel_to_point(depth_intrinsics, coord, depth_image[pixel_y][pixel_x] * depth_scale)
    z = -z
    return [x, y, z]

def calculate_distance(list1, list2):  # Take two 2D points and calculate distance
    dist = float(math.sqrt((list1[0] - list2[0]) ** 2 + (list1[1] - list2[1]) ** 2))
    return dist  # in meter