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
# style.use("ggplot")

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
        self.entry_fi1_min = -90
        self.entry_fi1_max = 90
        self.entry_fi2_min = -50
        self.entry_fi2_max = 125
        self.entry_fi3_min = 0
        self.entry_fi3_max = 120
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
        self.subplot_obalka_yz.grid()



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
        l1 = 203.0  # mm
        l2 = 178.0  # mm
        l3 = 178.0  # mm
        phi1_max = to_radian(self.entry_fi1_max)
        phi1_min = to_radian(self.entry_fi1_min)
        phi1_range = np.arange(phi1_min, phi1_max, delta_fi)
        closest_to_zero = min(abs(phi1_range))

        # phi1_range = [0.0]
        phi2_max = to_radian(self.entry_fi2_max)
        phi2_min = to_radian(self.entry_fi2_min)
        phi2_range = np.arange(phi2_min, phi2_max, delta_fi)

        phi3_max = to_radian(self.entry_fi3_max)
        phi3_min = to_radian(self.entry_fi3_min)
        phi3_range = np.arange(phi3_min, phi3_max, delta_fi)
        length = len(phi1_range) * len(phi2_range) * len(phi3_range)
        list_a = np.zeros([4, length])
        list_b = np.zeros([4, length])
        list_c = np.zeros([4, length])
        list_c_fi_in_zero = np.zeros([4, len(phi2_range) * len(phi3_range)])

        index = 0
        index0 = 0
        for fi1 in phi1_range:
            for fi2 in phi2_range:
                for fi3 in phi3_range:
                    a, b, c = self.manipulator.calculate_position_from_temp_data(fi1, fi2, fi3, l1, l2, l3)
                    list_a[:, index] = a[:, 0]
                    list_b[:, index] = b[:, 0]
                    list_c[:, index] = c[:, 0]
                    if fi1 == closest_to_zero:
                        list_c_fi_in_zero[:, index0] = c[:, 0]
                        index0 += 1
                    index = index + 1

        # print(str(index))

        self.subplot_obalka_yz.set_title("Pracovny priestor v rovine Y0Z")
        self.subplot_obalka_yz.plot(list_c_fi_in_zero[1, :], list_c_fi_in_zero[2, :], 'o', lw=0.1)
        self.subplot_obalka_yz.set_xlabel('y')
        self.subplot_obalka_yz.set_ylabel('z')

        self.subplot_obalka_xy.set_title("Pracovny priestor v rovine X0Y")
        self.subplot_obalka_xy.plot(list_c[1, :], list_c[0, :], 'o', lw=0.1)
        self.subplot_obalka_xy.set_xlabel('y')
        self.subplot_obalka_xy.set_ylabel('x')

    def vykresli(self):
        self.subplot_obalka_yz.clear()
        self.subplot_obalka_xy.clear()
        self.draw_robot_work_area_yz()

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
        self.subplot_obalka_xy.set_xlabel('x')
        self.subplot_obalka_xy.set_ylabel('y')

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
        try:
            self.entry_fi1 = float(self.app_frame.entry11.get())*np.pi/180
            self.entry_fi2 = float(self.app_frame.entry12.get())*np.pi/180
            self.entry_fi3 = float(self.app_frame.entry13.get())*np.pi/180
            self.entry_l1 = float(self.app_frame.entry21.get())/1000
            self.entry_l2 = float(self.app_frame.entry22.get())/1000
            self.entry_l3 = float(self.app_frame.entry23.get())/1000
            self.entry_fi1_min = float(self.app_frame.entry_fi1_min.get())
            self.entry_fi1_max = float(self.app_frame.entry_fi1_max.get())
            self.entry_fi2_min = float(self.app_frame.entry_fi2_min.get())
            self.entry_fi2_max = float(self.app_frame.entry_fi2_max.get())
            self.entry_fi3_min = float(self.app_frame.entry_fi3_min.get())
            self.entry_fi3_max = float(self.app_frame.entry_fi3_max.get())
        except ValueError:
            Label(self, text='Naespravne zadane udaje', fg="red").grid(row=6, column=1, columnspan=3)
            # errormsg.grid(row=6, column=1, columnspan=3)

        self.manipulator.set_fi1(self.entry_fi1)
        self.manipulator.set_fi2(self.entry_fi2)
        self.manipulator.set_fi3(self.entry_fi3)
        self.manipulator.set_l1(self.entry_l1)
        self.manipulator.set_l2(self.entry_l2)
        self.manipulator.set_l3(self.entry_l3)
        # self.manipulator.fi1, self.manipulator.fi2, self.manipulator.fi3, self.manipulator.l1, self.manipulator.l2, self.manipulator.l3 = self.app_frame.get_fis_and_ls()
        self.manipulator.calculate_position()
        # self.subplot3d.clear()

        # self.subplot3d.view_init(self.var_scale1, 30)
        self.draw_in_3d()

        # self.draw_robot_work_area_yz()
        # self.draw_robot_work_area_xy()

        # self.test_draw()

        self.canvas.get_tk_widget().pack(side=RIGHT)
        # self.app_frame.initUI()
        # print("Vykreslujem...")

    def test_draw(self):
        self.subplot3d.plot([1, 2, 3, 4, 5, 6, 7], [9, 8, 7, 6, 5, 4, 3], [5, 6, 9, 8, 7, 4, 1], 'r-')

    def work_panel(self):
        # self.waiting = Label(self, text='Prebieha vypocet...', fg="red")
        kresli = Button(self.app_frame, text='Vykresli', command=self.vykresli)
        kresli.grid(row=12, column=1, columnspan=3)
        Button(self.app_frame, text='Quit', command=self.quit).grid(row=13, column=1, columnspan=3, pady=20)

        # ============ 2. Cast=======
    #     self.scale1 = Scale(self.app_frame, from_=0, to_=50, command=self.on_scale1)
    #     self.scale1.grid(row=7, column=1, columnspan=2, padx=5)
    #     self.var_scale1 = IntVar()
    #     self.label_scale1 = Label(self.app_frame, text=0, textvariable=self.var_scale1)
    #     self.label_scale1.grid(row=7, column=3, sticky=W + E)
    #
    # def on_scale1(self, val):
    #     v = int(float(val))
    #     self.var_scale1.set(v)

    def animate(self, i):
        self.subplot3d.clear()
        # self.subplot_obalka_yz.clear()
        # self.subplot_obalka_xy.clear()
        self.update()
        # t = self.subplot3d.get_init()
        # self.subplot3d.mouse_init()
        # self.subplot3d.view_init(-140, 60)
        # self.subplot_obalka_yz.mouse_init()


class Frames(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.initUI()

    # def get_fis_and_ls(self):
    #     return self.entry_fi1, self.entry_fi2, self.entry_fi3, self.entry_l1, self.entry_l2, self.entry_l3

    def initUI(self):
        self.master.title("Zadanie robotika")
        self.pack(side=LEFT, fill=BOTH, expand=True)

        self.columnconfigure(0, pad=0)
        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2)
        self.columnconfigure(4, pad=10)
        # self.columnconfigure(3, weight=1)

        for i in range(1, 13):
            self.rowconfigure(i, pad=5)

        label1 = Label(self, text="Interaktivne polohovanie manipulatora")
        label1.grid(row=0, column=1, columnspan=3, pady=10, padx=2, sticky=E+W+N+S)

        Label(self, text="Fi_1 [°]").grid(row=1, column=1, padx=0, pady=0, sticky=W+E)
        Label(self, text="Fi_2 [°]").grid(row=1, column=2, padx=0, pady=0, sticky=W+E)
        Label(self, text="Fi_3 [°]").grid(row=1, column=3, padx=0, pady=0, sticky=W+E)

        self.entry11 = Entry(self)
        self.entry12 = Entry(self)
        self.entry13 = Entry(self)

        self.entry11.grid(row=2, column=1, padx=0, pady=0, sticky=W+E)
        self.entry12.grid(row=2, column=2, padx=0, pady=0, sticky=W+E)
        self.entry13.grid(row=2, column=3, padx=0, pady=0, sticky=W+E)

        self.entry11.insert(0, self.master.entry_fi1)
        self.entry12.insert(0, self.master.entry_fi2)
        self.entry13.insert(0, self.master.entry_fi3)

        # ====
        label_entry_l1 = Label(self, text="L_1 [mm]")
        label_entry_l2 = Label(self, text="L_2 [mm]")
        label_entry_l3 = Label(self, text="L_3 [mm]")

        self.entry21 = Entry(self)
        self.entry22 = Entry(self)
        self.entry23 = Entry(self)

        label_entry_l1.grid(row=3, column=1, padx=0, pady=0, sticky=W + E)
        label_entry_l2.grid(row=3, column=2, padx=0, pady=0, sticky=W + E)
        label_entry_l3.grid(row=3, column=3, padx=0, pady=0, sticky=W + E)
        self.entry21.grid(row=4, column=1, padx=0, pady=0, sticky=W + E)
        self.entry22.grid(row=4, column=2, padx=0, pady=0, sticky=W + E)
        self.entry23.grid(row=4, column=3, padx=0, pady=0, sticky=W + E)

        self.entry21.insert(0, self.master.entry_l1)
        self.entry22.insert(0, self.master.entry_l2)
        self.entry23.insert(0, self.master.entry_l3)



        #============ 2. Cast=======
        label1 = Label(self, text="Pracovny priestor")
        label1.grid(row=5, column=1, columnspan=2, pady=10, padx=2, sticky=E + W + N + S)

        Label(self, text="Fi_{1} min [°]").grid(row=6, column=1, padx=0, pady=0, sticky=W + E)
        Label(self, text="Fi_{1} max [°]").grid(row=6, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi1_min = Entry(self)
        self.entry_fi1_max = Entry(self)

        self.entry_fi1_min.grid(row=7, column=1, padx=0, pady=0, sticky=W + E)
        self.entry_fi1_max.grid(row=7, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi1_min.insert(0, self.master.entry_fi1_min)
        self.entry_fi1_max.insert(0, self.master.entry_fi1_max)

        ####=========================== FI2
        Label(self, text="Fi_{2} min [°]").grid(row=8, column=1, padx=0, pady=0, sticky=W + E)
        Label(self, text="Fi_{2} max [°]").grid(row=8, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi2_min = Entry(self)
        self.entry_fi2_max = Entry(self)

        self.entry_fi2_min.grid(row=9, column=1, padx=0, pady=0, sticky=W + E)
        self.entry_fi2_max.grid(row=9, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi2_min.insert(0, self.master.entry_fi2_min)
        self.entry_fi2_max.insert(0, self.master.entry_fi2_max)

        ####=========================== FI3 =============================
        Label(self, text="Fi_{3} min [°]").grid(row=10, column=1, padx=0, pady=0, sticky=W + E)
        Label(self, text="Fi_{3} max [°]").grid(row=10, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi3_min = Entry(self)
        self.entry_fi3_max = Entry(self)

        self.entry_fi3_min.grid(row=11, column=1, padx=0, pady=0, sticky=W + E)
        self.entry_fi3_max.grid(row=11, column=2, padx=0, pady=0, sticky=W + E)

        self.entry_fi3_min.insert(0, self.master.entry_fi3_min)
        self.entry_fi3_max.insert(0, self.master.entry_fi3_max)

        #============ Suradnicove systemy =========
        label1 = Label(self, text="Suradnicove systemy")
        label1.grid(row=14, column=1, columnspan=2, pady=10, padx=2, sticky=E + W + N + S)







