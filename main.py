import numpy as np
import matplotlib.animation as animation
from gui import Root
from manipulator import Manipulator


def to_radian(x):
    return (x * np.pi)/180


"""
            UVODNE NASTAVOVACKY
"""
delta_fi = 0.1
# parametre manipulatora
l1 = 203.0  # mm
l2 = 178.0  # mm
l3 = 178.0  # mm
phi1_max = to_radian(90)
phi1_min = to_radian(-90)
phi1_range = np.arange(phi1_min, phi1_max, delta_fi)
# phi1_range = [0.0]

phi2_max = to_radian(125)
phi2_min = to_radian(-55)
phi2_range = np.arange(phi2_min, phi2_max, delta_fi)

phi3_max = to_radian(150)
phi3_min = to_radian(0)
phi3_range = np.arange(phi3_min, phi3_max, delta_fi)
length = len(phi1_range) * len(phi2_range) * len(phi3_range)

robot = Manipulator(l1, l2, l3)

A = np.zeros([4, length])
B = np.zeros([4, length])
C = np.zeros([4, length])

# index = 0
# for fi1 in phi1_range:
#     robot.fi1 = fi1
#     for fi2 in phi2_range:
#         robot.fi2 = fi2
#         for fi3 in phi3_range:
#             robot.fi3 = fi3
#             a, b, c = robot.calculate_position()
#             A[:, index] = a[:, 0]
#             B[:, index] = b[:, 0]
#             C[:, index] = c[:, 0]
#             index = index + 1


if __name__ == '__main__':
    root = Root(robot)
    ani = animation.FuncAnimation(root.figure, root.animate, interval=1000)
    # root.update()
    root.mainloop()
