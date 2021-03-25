import pygame
import numpy as np
import drawing
import funkcie
import Points


"""
    Program pre vykreslenie pohybu robotickeho manipulatora
"""


def to_radian(x):
    return (x * np.pi)/180


delta_fi = 0.1
# parametre manipulatora
l1 = 203.0
l2 = 178.0
l3 = 178.0
phi1_max = to_radian(90)
phi1_min = to_radian(-90)
phi1_range = np.arange(phi1_min, phi1_max, delta_fi)

phi2_max = to_radian(125)
phi2_min = to_radian(-55)
phi2_range = np.arange(phi2_min, phi2_max, delta_fi)

phi3_max = to_radian(150)
phi3_min = to_radian(0)
phi3_range = np.arange(phi3_min, phi3_max, delta_fi)

# nastavenie pygame window
sirka_okna = 1000  # 1920
vyska_okna = 800  # 1080
SIZE = (sirka_okna, vyska_okna)
fps = 30
start_point = (int(sirka_okna/2), int(vyska_okna/1.5))
x_offset = start_point[0]
y_offset = start_point[1]

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen1 = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Zadanie c. 1 - Robotika")
icon = pygame.image.load('industrial_robot.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

scatter_c_yz = []

# Vypocet
A = np.ones((4, len(phi1_range)*len(phi2_range)*len(phi3_range)))
B = np.ones((4, len(phi1_range)*len(phi2_range)*len(phi3_range)))
C = np.ones((4, len(phi1_range)*len(phi2_range)*len(phi3_range)))
print(str(len(phi1_range)*len(phi2_range)*len(phi3_range)))
# idx = 0
# for i in range(len(phi1_range)-1):
#     for j in range(len(phi2_range)-1):
#         for k in range(len(phi3_range)-1):
#             A[:, idx], B[:, idx], C[:, idx] = funkcie.calculate_manipulator_position(phi1_range[i],
#                                                                                      phi2_range[j],
#                                                                                      phi3_range[k],
#                                                                                      l1, l2, l3)
#             idx = idx + 1

"""
# ordered iterating
if self.loop:
    self.fi_1 = self.fi_1 + 0.1
    if self.fi_1 > self.fi_1_limit[1]:
        self.fi_1 = self.fi_1_limit[0]
        self.fi_2 = self.fi_2 + 0.1
        if self.fi_2 > self.fi_2_limit[1]:
            self.fi_2 = self.fi_2_limit[0]
            self.fi_3 = self.fi_3 + 0.1
            if self.fi_3 > self.fi_3_limit[1]:
                self.loop = False
"""
fi_1 = phi1_min
fi_2 = phi2_min
fi_3 = phi3_min
loop = True
idx = 0
run = True
while run:
    clock.tick(fps)
    screen1.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw = drawing.Drawing(x_offset, y_offset, screen1)
    draw.draw_axes()

    # ordered iterating
    if loop:
        fi_1 = fi_1 + delta_fi
        if fi_1 > phi1_max:
            fi_1 = phi1_min
            fi_2 = fi_2 + delta_fi
            if fi_2 > phi2_max:
                fi_2 = phi2_min
                fi_3 = fi_3 + delta_fi
                if fi_3 > phi3_max:
                    loop = False
                    run = False

    A[:, idx], B[:, idx], C[:, idx] = funkcie.calculate_manipulator_position(fi_1, fi_2, fi_3, l1, l2, l3)
    draw.draw_manipulator(A[:, idx], B[:, idx], C[:, idx])

    if idx < len(phi1_range)*len(phi2_range)*len(phi3_range):
        idx = idx + 1
    else:
        idx = 0
    # print(str(idx))
    pygame.display.update()




