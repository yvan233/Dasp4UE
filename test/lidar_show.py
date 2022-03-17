import numpy as np
from matplotlib import pyplot as plt


def parsePointcloud(point_array):
    x_points = []
    y_points = []
    z_points = []
    for i in range(0, point_array.shape[0], 3):
        x_points.append(point_array[i])
        y_points.append(point_array[i + 1])
        z_points.append(point_array[i + 2]) 
    return x_points, y_points, z_points


if __name__ == '__main__':
    file_path = "D:/Qiyuan/Record/2022-03-17-19-42-21/pointcloud/pointcloud_1647517294868.npy"
    pointcloud = np.load(file_path)
    x_points, y_points, z_points = parsePointcloud(pointcloud)
    plt.figure(figsize=(8, 6))
    ax = plt.axes(projection='3d')
    # 现在场景中z轴向下
    ax.scatter3D(x_points, y_points, z_points)
    plt.show()