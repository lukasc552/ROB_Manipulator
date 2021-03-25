import numpy as np
import matplotlib.pyplot as plt
from manipulator import Manipulator


def init():
    pass


def animate(i):
    pass


def to_radian(x):
    return (x * np.pi)/180

# ==================== NASTAVOVACKY ===================
delta_fi = 0.2
# parametre manipulatora
l1 = 203.0  # mm
l2 = 178.0  # mm
l3 = 178.0  # mm
phi1_max = to_radian(90)
phi1_min = to_radian(-90)
# phi1_range = np.arange(phi1_min, phi1_max, delta_fi)
phi1_range = [0.0]

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

index = 0
for fi1 in phi1_range:
    for fi2 in phi2_range:
        for fi3 in phi3_range:
            a, b, c = robot.calculate_position(fi1, fi2, fi3)
            A[:, index] = a[:, 0]
            B[:, index] = b[:, 0]
            C[:, index] = c[:, 0]
            index = index + 1


figure = plt.figure(figsize=(12, 6), dpi=100)
sub11 = plt.subplot(121)
sub11.title.set_text('Pohlad zboku (rovina Y0Z)')
robot.draw_manipulator_2d(sub11, A[:, 0], B[:, 0], C[:, 0])

sub12 = figure.add_subplot(122, projection='3d')
sub12.title.set_text('Pohlad zhora (rovina X0Y)')

# plt.show()



# fig = plt.figure(2)
# ax = axes3d.Axes3D(figure)
# Setting the axes properties
sub12.set_xlim3d([-400, 500])
sub12.set_xlabel('X')
sub12.set_ylim3d([-400, 500])
sub12.set_ylabel('Y')
sub12.set_zlim3d([-100, 600])
sub12.set_zlabel('Z')
sub12.set_title('3D Manipulator')
alpha = 0.8
sub12.scatter(C[0, :], C[1, :], C[2, :], 'o-', lw=1, alpha=alpha)


plt.show()
