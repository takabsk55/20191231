# -*- coding:utf-8 -*-

import tkinter
import numpy as np
import numpy
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class Scribble:
    # ボタンが押された
    prex = 0
    prey = 0
    precolor = 0

    redx = []
    redy = []
    greenx = []
    greeny = []

    def on_pressed(self, event):
        if self.precolor != self.color.get():
            self.sx = event.x
            self.sy = event.y
            if self.color.get() == "red":
                self.redx = []
                self.redy = []
                self.canvas.delete("red")
                self.canvas.create_oval(event.x, event.y, event.x, event.y,
                                        outline=self.color.get(),
                                        width=self.width.get(), tag="red")
                self.redx.append(self.sx)
                self.redy.append(self.sy)

            if self.color.get() == "green":
                self.greenx = []
                self.greeny = []
                self.canvas.delete("green")
                self.canvas.create_oval(event.x, event.y, event.x, event.y,
                                        outline=self.color.get(),
                                        width=self.width.get(), tag="green")
                self.greenx.append(self.sx)
                self.greeny.append(self.sy)

            self.prex = event.x
            self.prey = event.y
            self.precolor = self.color.get()

        else:
            self.sx = event.x
            self.sy = event.y
            if self.color.get() == "red":
                self.canvas.create_oval(self.sx, self.sy, event.x, event.y,
                                        outline=self.color.get(),
                                        width=self.width.get(), tag="red")
                self.canvas.create_line(self.prex, self.prey, event.x, event.y,
                                        fill=self.color.get(),
                                        width=self.width.get(), tag="red")
                self.redx.append(self.sx)
                self.redy.append(self.sy)

            if self.color.get() == "green":
                self.canvas.create_oval(self.sx, self.sy, event.x, event.y,
                                        outline=self.color.get(),
                                        width=self.width.get(), tag="green")
                self.canvas.create_line(self.prex, self.prey, event.x, event.y,
                                        fill=self.color.get(),
                                        width=self.width.get(), tag="green")
                self.greenx.append(self.sx)
                self.greeny.append(self.sy)

            self.prex = event.x
            self.prey = event.y

    # ウィンドウを作る
    def create_window(self):
        window = tkinter.Tk()

        self.canvas = tkinter.Canvas(window, background="white",
                                     width=600, height=600)

        self.canvas.pack()

        quit_button = tkinter.Button(window, text="終了",
                                     command=window.quit)
        quit_button.pack(side=tkinter.RIGHT)

        calc_button = tkinter.Button(window, text="計算", command=self.DTW)
        calc_button.pack(side=tkinter.RIGHT)

        self.canvas.bind("<ButtonPress-1>", self.on_pressed)

        # 色を選ぶ
        COLORS = ["red", "green"]
        self.color = tkinter.StringVar()
        self.color.set(COLORS[1])
        b = tkinter.OptionMenu(window, self.color, *COLORS)
        b.pack(side=tkinter.LEFT)

        self.width = tkinter.Scale(window, from_=1, to=15,
                                   orient=tkinter.HORIZONTAL)
        self.width.set(5)
        self.width.pack(side=tkinter.LEFT)

        return window;

    def run(self):
        self.window.mainloop()

    def doubleerror(self, a, b):
        return (a - b) ** 2

    def disterror(self, ansx, ansy, gpsx, gpsy):
        return ((ansx - gpsx) ** 2 + (ansy - gpsy) ** 2) ** 0.5

    def first(self, x):
        return x[0]

    def second(self, x):
        return x[1]

    def calc_dtw(self, redx, redy, greenx, greeny):
        S = len(redx)
        T = len(greenx)

        m = [[(0, (0, 0)) for j in range(T)] for i in range(S)]
        m[0][0] = (self.disterror(redx[0], redy[0], greenx[0], greeny[0]), (-1, -1))
        for i in range(1, S):
            m[i][0] = (m[i - 1][0][0] + self.disterror(redx[i], redy[i], greenx[0], greeny[0]), (i - 1, 0))
        for j in range(1, T):
            m[0][j] = (m[0][j - 1][0] + self.disterror(redx[0], redy[0], greenx[j], greeny[j]), (0, j - 1))
        for i in range(1, S):

            for j in range(1, T):

                minimum, index = self.minVal(m[i - 1][j], m[i][j - 1], m[i - 1][j - 1])
                indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
                m[i][j] = (self.first(minimum) + self.disterror(redx[i], redy[i], greenx[j], greeny[j]), indexes[index])
        return m

    def minVal(self, v1, v2, v3):
        if self.first(v1) <= min(self.first(v2), self.first(v3)):
            return v1, 0
        elif self.first(v2) <= self.first(v3):
            return v2, 1
        else:
            return v3, 2

    def backward(self, m):
        path = []
        path.append([len(m) - 1, len(m[0]) - 1])
        while True:

            if path[-1][0] - path[-1][1] > 5:
                path.append(m[path[-1][0] - 1][path[-1][1]][1])
                continue
            if path[-1][1] - path[-1][0] > 5:
                path.append(m[path[-1][0]][path[-1][1] - 1][1])
                continue

            path.append(m[path[-1][0]][path[-1][1]][1])
            if path[-1] == (0, 0):
                break
        path = np.array(path)
        return path

    def plot_path(self, path, redx, redy, greenx, greeny):

        plt.figure()

        ax = plt.subplot()
        ax.set_ylim([0, 600])
        ax.set_xlim([0, 600])
        ax.set_aspect('equal')
        for line in path:
            plt.plot([greenx[line[1]], redx[line[0]]], [600 - greeny[line[1]], 600 - redy[line[0]]], linewidth=0.8,
                     c="gray")

        redy = list(map(lambda x: x * -1 + 600, redy))
        greeny = list(map(lambda x: x * -1 + 600, greeny))

        plt.plot(redx, redy, color="Red")
        plt.plot(greenx, greeny, color="Green")

        ax.annotate("s", (redx[0], redy[0]), color="Blue")
        ax.annotate("e", (redx[-1], redy[-1]), color="Blue")

        ax.annotate("s", (greenx[0], greeny[0]), color="Blue")
        ax.annotate("e", (greenx[-1], greeny[-1]), color="Blue")

        plt.savefig("DTW")

        return

    def DTW(self):

        m = self.calc_dtw(self.redx, self.redy, self.greenx, self.greeny)
        path = self.backward(m)
        self.plot_path(path, self.redx, self.redy, self.greenx, self.greeny)

        return path

    def __init__(self):
        self.window = self.create_window();  # 呼び出すときはself. + メソッド名


# 開始
Scribble().run()
