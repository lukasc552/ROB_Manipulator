import pygame

white = (255, 255, 255)
black = (0, 0, 0)
green = (20, 200, 30)
red = (255, 0, 0)
yellow = (255, 255, 0)


class Drawing:
    def __init__(self, start_x, start_y, surface):
        self.start_x = start_x
        self.start_y = start_y
        self.start_point = (start_x, start_y)  # eq. (x, y)
        self.surface = surface
        self.axes_color = white
        self.manipulator_color = red
        self.points_color = yellow

    def draw_axes(self):
        # z-ova os
        pygame.draw.line(self.surface, self.axes_color, self.start_point, (self.start_x, self.start_y - 500), 2)

        # y-ova os
        pygame.draw.line(self.surface, self.axes_color, self.start_point, (self.start_x + 500, self.start_y), 2)

    def draw_manipulator(self, point_a, point_b, point_c):
        yz_point_a = (self.start_x + point_a[1], self.start_y - point_a[2])
        yz_point_b = (self.start_x + point_b[1], self.start_y - point_b[2])
        yz_point_c = (self.start_x + point_c[1], self.start_y - point_c[2])

        pygame.draw.line(self.surface, self.manipulator_color, self.start_point, yz_point_a, 6)
        pygame.draw.circle(self.surface, self.manipulator_color, yz_point_a, 10)

        pygame.draw.line(self.surface, self.manipulator_color, yz_point_a, yz_point_b, 6)
        pygame.draw.circle(self.surface, self.manipulator_color, yz_point_b, 10)

        pygame.draw.line(self.surface, self.manipulator_color, yz_point_b, yz_point_c, 6)
        pygame.draw.circle(self.surface, self.manipulator_color, yz_point_c, 10)

    def draw_points_yz(self, coords):
        # if len(coordinates) > 2:
        for coord in coords:
            # coordinates1, coordinates2 = self.start_x + coords[:, 0], self.start_y - coords[:, 1]
            x = self.start_x + coord[0]
            y = self.start_y - coord[1]
            pygame.draw.line(self.surface, self.points_color, x, y, 2)
