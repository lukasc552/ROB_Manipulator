import numpy as np


def calculate_manipulator_position(fi1, fi2, fi3, l1, l2, l3):
    # A = np.ones([4, 1])
    # B = np.ones([4, 1])
    # C = np.ones([4, 1])
    a = np.array([[0],
                  [0],
                  [l1],
                  [1]])
    b = np.array([[0],
                  [0],
                  [l2],
                  [1]])
    c = np.array([[0],
                  [0],
                  [l3],
                  [1]])

    R_z_fi1 = np.array([[np.sin(fi1), -np.cos(fi1), 0, 0],
                        [np.cos(fi1), np.sin(fi1), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

    T_z_l1 = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, l1],
                       [0, 0, 0, 1]])

    R_y_fi2 = np.array([[np.cos(fi2), 0, np.sin(fi2), 0],
                        [0, 1, 0, 0],
                        [-np.sin(fi2), 0, np.cos(fi2), 0],
                        [0, 0, 0, 1]])

    T_z_l2 = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, l2],
                       [0, 0, 0, 1]])

    R_y_fi3 = np.array([[np.cos(fi3), 0, np.sin(fi3), 0],
                        [0, 1, 0, 0],
                        [-np.sin(fi3), 0, np.cos(fi3), 0],
                        [0, 0, 0, 1]])

    # p5_l3 = np.array([[0],
    #                   [0],
    #                   [l3],
    #                   [1]])
    #  pre bod A
    A = np.matmul(R_z_fi1, a)

    #  pre bod B
    B = np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), b)

    #  pre bod C
    C = np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), T_z_l2), R_y_fi3), c)
    # print(str(C))
    return A.T, B.T, C.T
