import numpy as np
from tkinter import *
from tkinter.ttk import Frame
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.style as style

matplotlib.use("TkAgg")
# style.use("dark_background")

# figure = plt.Figure(figsize=(5, 5), dpi=100)
# subplot3d = figure.add_subplot(111, projection='3d')


def to_radian(x):
    return (x * np.pi)/180


class Root(Tk):
    def __init__(self, robot):
        super(Root, self).__init__()
        self.minsize(800, 600)
        self.manipulator = robot

        self.ndim = 3
        self.entry_fi1 = 30
        self.entry_fi2 = 45
        self.entry_fi3 = 30
        self.entry_l1 = 203
        self.entry_l2 = 178
        self.entry_l3 = 178
        # self.fi1 = -30 * np.pi / 180
        # self.fi2 = 45 * np.pi / 180
        # self.fi3 = 30 * np.pi / 180

        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.subplot3d = self.figure.add_subplot(221, projection='3d')
        self.subplot3d.view_init(20, 30)

        # self.subplot3d.mouse_init()
        self.subplot_obalka_yz = self.figure.add_subplot(223)
        self.subplot_obalka_yz.grid()


        self.subplot_obalka_xy = self.figure.add_subplot(224)




        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()

        # self.canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
        # self.canvas.mpl_connect("key_press_event", key_press_handler)

        # self.canvas.pick(MouseEvent)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=RIGHT, expand=True)
        # self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        self.app_frame = Frames(self)
        self.work_panel()

    def draw_robot_work_area_yz(self, delta_fi = 0.1):
        # phi1_max = to_radian(90)
        # phi1_min = to_radian(-90)
        # phi1_range = np.arange(phi1_min, phi1_max, delta_fi)
        l1 = 203.0  # mm
        l2 = 178.0  # mm
        l3 = 178.0  # mm
        phi1_range = [0.0]
        phi2_max = to_radian(125)
        phi2_min = to_radian(-55)
        phi2_range = np.arange(phi2_min, phi2_max, delta_fi)

        phi3_max = to_radian(150)
        phi3_min = to_radian(0)
        phi3_range = np.arange(phi3_min, phi3_max, delta_fi)
        length = len(phi1_range) * len(phi2_range) * len(phi3_range)
        list_a = np.zeros([4, length])
        list_b = np.zeros([4, length])
        list_c = np.zeros([4, length])

        index = 0
        for fi1 in phi1_range:
            for fi2 in phi2_range:
                for fi3 in phi3_range:
                    a, b, c = self.manipulator.calculate_position_from_temp_data(fi1, fi2, fi3, l1, l2, l3)
                    list_a[:, index] = a[:, 0]
                    list_b[:, index] = b[:, 0]
                    list_c[:, index] = c[:, 0]
                    index = index + 1

        # print(str(index))

        self.subplot_obalka_yz.set_title("Pracovny priestor v rovine Y0Z")
        self.subplot_obalka_yz.plot(list_c[1, :], list_c[2, :], 'o', lw=0.4)
        self.subplot_obalka_yz.set_xlabel('y')
        self.subplot_obalka_yz.set_ylabel('z')

    def draw_robot_work_area_xy(self, delta_fi = 0.1):
        l1 = 203.0  # mm
        l2 = 178.0  # mm
        l3 = 178.0  # mm
        phi1_max = to_radian(90)
        phi1_min = to_radian(-90)
        phi1_range = np.arange(phi1_min, phi1_max, delta_fi)
        phi2_max = to_radian(125)
        phi2_min = to_radian(-55)
        phi2_range = np.arange(phi2_min, phi2_max, delta_fi)

        phi3_max = to_radian(150)
        phi3_min = to_radian(0)
        phi3_range = np.arange(phi3_min, phi3_max, delta_fi)
        length = len(phi1_range) * len(phi2_range) * len(phi3_range)
        list_a = np.zeros([4, length])
        list_b = np.zeros([4, length])
        list_c = np.zeros([4, length])

        index = 0
        for fi1 in phi1_range:
            for fi2 in phi2_range:
                for fi3 in phi3_range:
                    a, b, c = self.manipulator.calculate_position_from_temp_data(fi1, fi2, fi3, l1, l2, l3)
                    # list_a[:, index] = a[:, 0]
                    # list_b[:, index] = b[:, 0]
                    list_c[:, index] = c[:, 0]
                    index = index + 1

        self.subplot_obalka_xy.set_title("Pracovny priestor v rovine Y0Z")
        self.subplot_obalka_xy.plot(list_c[0, :], list_c[1, :], 'o', lw=0.4)
        self.subplot_obalka_xy.set_xlabel('x', align='horizontal')
        self.subplot_obalka_xy.set_ylabel('y', align='vertical')

    def draw_in_2d(self):
        A = self.manipulator.pos_a
        B = self.manipulator.pos_b
        C = self.manipulator.pos_c
        self.manipulator.draw_manipulator_2d(self.subplot3d, A, B, C)

    def draw_in_3d(self):
        A = self.manipulator.pos_a
        B = self.manipulator.pos_b
        C = self.manipulator.pos_c
        # print("A: " + str(self.manipulator.pos_a))
        # print("B: " + str(self.manipulator.pos_b))
        # print("C: " + str(self.manipulator.pos_c))
        self.subplot3d.set_title("Pozicia manipulatora v 3D priestore")
        self.manipulator.draw_manipulator_3d(self.subplot3d, A, B, C)
        # self.subplot3d.set_animated(True)

    def update(self):
        # temp_fi1 = self.app_frame.entry_fi1
        # temp_fi2 = self.app_frame.entry_fi2
        # temp_fi3 = self.app_frame.entry_fi3
        # temp_l1 = self.app_frame.entry_l1
        # temp_l2 = self.app_frame.entry_l2
        # temp_l3 = self.app_frame.entry_l3

        try:
            self.entry_fi1 = float(self.app_frame.entry11.get())*np.pi/180
            self.entry_fi2 = float(self.app_frame.entry12.get())*np.pi/180
            self.entry_fi3 = float(self.app_frame.entry13.get())*np.pi/180
            self.entry_l1 = float(self.app_frame.entry21.get())/1000
            self.entry_l2 = float(self.app_frame.entry22.get())/1000
            self.entry_l3 = float(self.app_frame.entry23.get())/1000
        except ValueError:
            errormsg = Label(self, text='Naespravne zadane udaje', fg="red")
            errormsg.grid(row=6, column=1, columnspan=3)

        self.manipulator.set_fi1(self.entry_fi1)
        self.manipulator.set_fi2(self.entry_fi2)
        self.manipulator.set_fi3(self.entry_fi3)
        self.manipulator.set_l1(self.entry_l1)
        self.manipulator.set_l2(self.entry_l2)
        self.manipulator.set_l3(self.entry_l3)
        # self.manipulator.fi1, self.manipulator.fi2, self.manipulator.fi3, self.manipulator.l1, self.manipulator.l2, self.manipulator.l3 = self.app_frame.get_fis_and_ls()
        self.manipulator.calculate_position()
        # self.subplot3d.clear()

        self.draw_in_3d()
        self.draw_robot_work_area_yz()

        # self.test_draw()

        self.canvas.get_tk_widget().pack(side=RIGHT)
        # self.app_frame.initUI()
        # print("Vykreslujem...")

    def test_draw(self):
        self.subplot3d.plot([1, 2, 3, 4, 5, 6, 7], [9, 8, 7, 6, 5, 4, 3], [5, 6, 9, 8, 7, 4, 1], 'r-')

    def work_panel(self):
        # Button(self.app_frame, text='Vykresli', command=self.update).grid(row=5, column=1, columnspan=3)
        Button(self.app_frame, text='Quit', command=self.quit).grid(row=5, column=1, columnspan=3)
        # Button(self.app_frame, text='Quit', command=self.quit).grid(row=10, column=2, columnspan=2)
        # Button(self.master, )

    #     self.app_frame.initUI()
    #     button_vykresli = Button(self.app_frame, text='Vykresli', command=self.update)
    # @staticmethod
    def animate(self, i):
        self.subplot3d.clear()
        self.subplot_obalka_yz.clear()
        self.update()
        # t = self.subplot3d.get_init()
        # self.subplot3d.mouse_init()
        # self.subplot3d.view_init(-140, 60)
        # self.subplot_obalka_yz.mouse_init()


class Frames(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()
        # self.entry_fi1 = 10
        # self.entry_fi2 = 10
        # self.entry_fi3 = 10
        # self.entry_l1 = 10
        # self.entry_l2 = 10
        # self.entry_l3 = 10

        self.initUI()
        # print("FI1 v init-e: " + str(self.entry_fi1))
        # self.grid(sticky=E + W + N + S)
        #
        # top = self.winfo_toplevel()
        # top.rowconfigure(0, weight=1)
        # top.columnconfigure(0, weight=1)
        #
        # for i in range(10):
        #     self.rowconfigure(i, weight=1)
        #     self.columnconfigure(1, weight=1)

    def get_fis_and_ls(self):
        return self.entry_fi1, self.entry_fi2, self.entry_fi3, self.entry_l1, self.entry_l2, self.entry_l3

    def initUI(self):
        self.master.title("Zadanie robotika")
        self.pack(side=LEFT, fill=BOTH, expand=True)

        self.columnconfigure(0, pad=0)
        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2)
        self.columnconfigure(4, pad=10)
        # self.columnconfigure(3, weight=1)

        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)

        label1 = Label(self, text="Interaktivne polohovanie manipulatora")
        label1.grid(row=0, column=1, columnspan=3, pady=2, padx=2, sticky=E+W+N+S)

        label_entry_fi1 = Label(self, text="Fi_1 [C]").grid(row=1, column=1, padx=0, pady=0, sticky=W+E)
        label_entry_fi2 = Label(self, text="Fi_2 [C]").grid(row=1, column=2, padx=0, pady=0, sticky=W+E)
        label_entry_fi3 = Label(self, text="Fi_3 [C]").grid(row=1, column=3, padx=0, pady=0, sticky=W+E)
        # self.entry_fi1 = Entry(self)
        # self.entry_fi2 = Entry(self)
        # self.entry_fi3 = Entry(self)
        self.entry11 = Entry(self)
        # print(str(entry11))
        self.entry12 = Entry(self)
        self.entry13 = Entry(self)
        # print(str(entry11.get()))
        # self.entry_fi1 = entry11.getint(2)*np.pi/180
        # self.entry_fi2 = entry12.getint(2)*np.pi/180
        # self.entry_fi3 = entry13.getint(2)*np.pi/180

        self.entry11.grid(row=2, column=1, padx=0, pady=0, sticky=W+E)
        self.entry12.grid(row=2, column=2, padx=0, pady=0, sticky=W+E)
        self.entry13.grid(row=2, column=3, padx=0, pady=0, sticky=W+E)
        # print(type(self.entry11))
        self.entry11.insert(0, self.master.entry_fi1)
        self.entry12.insert(0, self.master.entry_fi2)
        self.entry13.insert(0, self.master.entry_fi3)

        # ====
        label_entry_l1 = Label(self, text="L_1 [mm]")
        label_entry_l2 = Label(self, text="L_2 [mm]")
        label_entry_l3 = Label(self, text="L_3 [mm]")
        # self.entry_l1 = Entry(self)
        # self.entry_l2 = Entry(self)
        # self.entry_l3 = Entry(self)
        self.entry21 = Entry(self)
        self.entry22 = Entry(self)
        self.entry23 = Entry(self)

        # self.entry_l1 = entry21.get()
        # self.entry_l2 = entry22.get()
        # self.entry_l3 = entry23.get()
        label_entry_l1.grid(row=3, column=1, padx=0, pady=0, sticky=W + E)
        label_entry_l2.grid(row=3, column=2, padx=0, pady=0, sticky=W + E)
        label_entry_l3.grid(row=3, column=3, padx=0, pady=0, sticky=W + E)
        self.entry21.grid(row=4, column=1, padx=0, pady=0, sticky=W + E)
        self.entry22.grid(row=4, column=2, padx=0, pady=0, sticky=W + E)
        self.entry23.grid(row=4, column=3, padx=0, pady=0, sticky=W + E)

        self.entry21.insert(0, self.master.entry_l1)
        self.entry22.insert(0, self.master.entry_l2)
        self.entry23.insert(0, self.master.entry_l3)

        # try:
        #     self.master.entry_fi1 = float(self.entry11.get())
        #     self.master.entry_fi2 = float(self.entry12.get())
        #     self.master.entry_fi3 = float(self.entry13.get())
        #     self.master.entry_l1 = float(self.entry21.get())
        #     self.master.entry_l2 = float(self.entry22.get())
        #     self.master.entry_l3 = float(self.entry23.get())
        # except ValueError:
        #     Label(self, text='Naespravne zadane udaje', fg="red")
    # print(str(self.master.entry_fi1))

        # self.master.entry_l1 = entry21.get()
        # self.master.entry_l2 = entry22.get()
        # self.master.entry_l3 = entry23.get()

    # def init_new_fi1(self):
#     button_vykresli.grid(row=5, column=3)








