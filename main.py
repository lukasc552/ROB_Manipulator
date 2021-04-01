import numpy as np
import matplotlib.animation as animation
from gui import Root
from manipulator import Manipulator


"""
            UVODNE NASTAVOVACKY
"""

l1 = 203.0  # mm
l2 = 178.0  # mm
l3 = 178.0  # mm
robot = Manipulator(l1, l2, l3)


if __name__ == '__main__':
    root = Root(robot)
    ani = animation.FuncAnimation(root.figure, root.animate, interval=1000)
    # root.update()
    root.mainloop()
