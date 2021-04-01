from typing import Any

import numpy as np


class Manipulator:
    def __init__(self, l1, l2, l3, x_offset=0.0, y_offset=0.0, z_offset=0.0):
        self.start_x = x_offset
        self.start_y = y_offset
        self.start_z = z_offset
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.fi1 = 30
        self.fi2 = 45
        self.fi3 = 30
        self.pos_a = np.array([[0.0], [0.0], [0.0], [1.0]])
        self.pos_b = np.array([[0.0], [0.0], [0.0], [1.0]])
        self.pos_c = np.array([[0.0], [0.0], [0.0], [1.0]])
        self.calculate_position()

    def set_fi1(self, value):
        self.fi1 = value

    def set_fi2(self, value):
        self.fi2 = value

    def set_fi3(self, value):
        self.fi3 = value

    def set_l1(self, value):
        self.l1 = value

    def set_l2(self, value):
        self.l2 = value

    def set_l3(self, value):
        self.l3 = value

    def get_fi1(self):
        return self.fi1

    def get_fi2(self):
        return self.fi2

    def get_fi3(self):
        return self.fi3

    def calculate_position(self):
        a = np.array([[0],
                      [0],
                      [self.l1],
                      [1]])
        b = np.array([[0],
                      [0],
                      [self.l2],
                      [1]])
        c = np.array([[0],
                      [0],
                      [self.l3],
                      [1]])

        R_z_fi1 = np.array([[np.sin(self.fi1), -np.cos(self.fi1), 0, 0],
                            [np.cos(self.fi1), np.sin(self.fi1), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        T_z_l1 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, self.l1],
                           [0, 0, 0, 1]])

        R_y_fi2 = np.array([[np.cos(self.fi2), 0, np.sin(self.fi2), 0],
                            [0, 1, 0, 0],
                            [-np.sin(self.fi2), 0, np.cos(self.fi2), 0],
                            [0, 0, 0, 1]])

        T_z_l2 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, self.l2],
                           [0, 0, 0, 1]])

        R_y_fi3 = np.array([[np.cos(self.fi3), 0, np.sin(self.fi3), 0],
                            [0, 1, 0, 0],
                            [-np.sin(self.fi3), 0, np.cos(self.fi3), 0],
                            [0, 0, 0, 1]])

        A = np.matmul(R_z_fi1, a)
        B = np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), b)
        C = np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), T_z_l2), R_y_fi3), c)
        self.pos_a[:, 0] = A[:, 0]
        self.pos_b[:, 0] = B[:, 0]
        self.pos_c[:, 0] = C[:, 0]

    def calculate_position_from_temp_data(self, temp_fi1=0.0, temp_fi2=0.0, temp_fi3=0.0, temp_l1=0.0, temp_l2=0.0, temp_l3=0.0):
        a = np.array([[0],
                      [0],
                      [temp_l1],
                      [1]])
        b = np.array([[0],
                      [0],
                      [temp_l2],
                      [1]])
        c = np.array([[0],
                      [0],
                      [temp_l3],
                      [1]])

        R_z_fi1 = np.array([[np.sin(temp_fi1), -np.cos(temp_fi1), 0, 0],
                            [np.cos(temp_fi1), np.sin(temp_fi1), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        T_z_l1 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, temp_l1],
                           [0, 0, 0, 1]])

        R_y_fi2 = np.array([[np.cos(temp_fi2), 0, np.sin(temp_fi2), 0],
                            [0, 1, 0, 0],
                            [-np.sin(temp_fi2), 0, np.cos(temp_fi2), 0],
                            [0, 0, 0, 1]])

        T_z_l2 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, temp_l2],
                           [0, 0, 0, 1]])

        R_y_fi3 = np.array([[np.cos(temp_fi3), 0, np.sin(temp_fi3), 0],
                            [0, 1, 0, 0],
                            [-np.sin(temp_fi3), 0, np.cos(temp_fi3), 0],
                            [0, 0, 0, 1]])

        A = np.matmul(R_z_fi1, a)
        B = np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), b)
        C = np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), T_z_l2), R_y_fi3), c)
        return A, B, C

    def draw_manipulator_2d(self, figure, point_a, point_b, point_c):
        body = [[self.start_y, point_a[1], point_b[1], point_c[1]],
                [self.start_z, point_a[2], point_b[2], point_c[2]]]

        figure.plot(body[0], body[1], 'r-', linewidth=6)

        # A koleno
        figure.plot(point_a[1], point_a[2], 'co', markersize=10)

        # B koleno
        figure.plot(point_b[1], point_b[2], 'co', markersize=9)

        # Bod C
        figure.plot(point_c[1], point_c[2], 'co', markersize=8)

    def draw_manipulator_3d(self, figure, point_a, point_b, point_c):
        body = np.array([[self.start_x, point_a[0, :], point_b[0, :], point_c[0, :]],
                         [self.start_y, point_a[1, :], point_b[1, :], point_c[1, :]],
                         [self.start_z, point_a[2, :], point_b[2, :], point_c[2, :]]], dtype=np.dtype(np.float64))

        figure.plot(body[0], body[1], body[2], 'r-', linewidth=4)
        figure.set_xlim3d([-0.2, 0.2])
        figure.set_ylim3d([-0.2, 0.2])
        figure.set_zlim3d([0, 0.5])
        figure.set_xticks([-0.2, -0.1, 0, 0.1, 0.2])
        figure.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
        figure.set_zticks([0, 0.1, 0.2, 0.3, 0.4])

        figure.set_xlabel('X[m]')
        figure.set_ylabel('Y[m]')
        figure.set_zlabel('Z[m]')
        # A koleno
        figure.plot(point_a[0], point_a[1], point_a[2], 'co', markersize=8)

        # B koleno
        figure.plot(point_b[0], point_b[1], point_b[2], 'co', markersize=6)

        # Bod C
        figure.plot(point_c[0], point_c[1], point_c[2], 'co', markersize=5)

    def draw_system(self, figure, k_sys = 0):
        R_z_fi1 = np.array([[np.sin(self.fi1), -np.cos(self.fi1), 0, 0],
                            [np.cos(self.fi1), np.sin(self.fi1), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        T_z_l1 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, self.l1],
                           [0, 0, 0, 1]])

        R_y_fi2 = np.array([[np.cos(self.fi2), 0, np.sin(self.fi2), 0],
                            [0, 1, 0, 0],
                            [-np.sin(self.fi2), 0, np.cos(self.fi2), 0],
                            [0, 0, 0, 1]])

        T_z_l2 = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, self.l2],
                           [0, 0, 0, 1]])

        R_y_fi3 = np.array([[np.cos(self.fi3), 0, np.sin(self.fi3), 0],
                            [0, 1, 0, 0],
                            [-np.sin(self.fi3), 0, np.cos(self.fi3), 0],
                            [0, 0, 0, 1]])

        line_size = 0.1
        x_vector = np.array([[line_size],
                             [0],
                             [0],
                             [1]])
        y_vector = np.array([[0],
                             [line_size],
                             [0],
                             [1]])
        z_vector = np.array([[0],
                             [0],
                             [line_size],
                             [1]])
        zero_vector = np.zeros([4, 1])
        empty_vector = np.array([[0],
                      [0],
                      [0],
                      [1]])
        x = np.zeros([4, 1])
        y = np.zeros([4, 1])
        z = np.zeros([4, 1])

        if k_sys == 0:
            x = x_vector
            y = y_vector
            z = z_vector
        elif k_sys == 1:
            x = np.matmul(R_z_fi1, x_vector)
            y = np.matmul(R_z_fi1, y_vector)
            z = np.matmul(R_z_fi1, z_vector)
        elif k_sys == 2:
            zero_vector = np.matmul(R_z_fi1, T_z_l1)
            x = np.matmul(zero_vector, x_vector)
            y = np.matmul(zero_vector, y_vector)
            z = np.matmul(zero_vector, z_vector)
            zero_vector = np.matmul(zero_vector, empty_vector)
        elif k_sys == 3:
            zero_vector = np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2)
            x = np.matmul(zero_vector, x_vector)
            y = np.matmul(zero_vector, y_vector)
            z = np.matmul(zero_vector, z_vector)
            zero_vector = np.matmul(zero_vector, empty_vector)
        elif k_sys == 4:
            zero_vector = np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), T_z_l2)
            x = np.matmul(zero_vector, x_vector)
            y = np.matmul(zero_vector, y_vector)
            z = np.matmul(zero_vector, z_vector)
            zero_vector = np.matmul(zero_vector, empty_vector)
        elif k_sys == 5:
            zero_vector = np.matmul(np.matmul(np.matmul(np.matmul(R_z_fi1, T_z_l1), R_y_fi2), T_z_l2), R_y_fi3)
            x = np.matmul(zero_vector, x_vector)
            y = np.matmul(zero_vector, y_vector)
            z = np.matmul(zero_vector, z_vector)
            zero_vector = np.matmul(zero_vector, empty_vector)

        # x-ova os
        figure.plot([zero_vector[0, 0], x[0, 0]], [zero_vector[1, 0], x[1, 0]], [zero_vector[2, 0], x[2, 0]], 'r-', linewidth=1)
        # y-ova os
        figure.plot([zero_vector[0, 0], y[0, 0]], [zero_vector[1, 0], y[1, 0]], [zero_vector[2, 0], y[2, 0]], 'g-', linewidth=1)
        # z-ova os
        figure.plot([zero_vector[0, 0], z[0, 0]], [zero_vector[1, 0], z[1, 0]], [zero_vector[2, 0], z[2, 0]], 'b-', linewidth=1)

    
