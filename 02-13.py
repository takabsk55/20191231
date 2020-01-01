# -*- coding:utf-8 -*-

import tkinter
import numpy as np
import numpy
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
class Scribble:
    # ボタンが押された
    prex=0
    prey=0
    precolor=0

    redx=[]
    redy=[]
    greenx=[]
    greeny=[]

    def on_pressed(self, event):
        if self.precolor!=self.color.get():
            self.sx = event.x
            self.sy = event.y
            if self.color.get()=="red":
                self.redx=[]
                self.redy=[]
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
                                    outline = self.color.get(),
                                    width = self.width.get(),tag="green")
                self.greenx.append(self.sx)
                self.greeny.append(self.sy)

            self.prex = event.x
            self.prey = event.y
            self.precolor=self.color.get()

        else:
            self.sx = event.x
            self.sy = event.y
            if self.color.get()=="red":

                self.canvas.create_oval(self.sx, self.sy, event.x, event.y,
                                        outline = self.color.get(),
                                        width = self.width.get(),tag="red")
                self.canvas.create_line(self.prex, self.prey, event.x, event.y,
                                        fill = self.color.get(),
                                        width = self.width.get(),tag="red")
                self.redx.append(self.sx)
                self.redy.append(self.sy)

            if self.color.get()=="green":

                self.canvas.create_oval(self.sx, self.sy, event.x, event.y,
                                        outline = self.color.get(),
                                        width = self.width.get(),tag="green")
                self.canvas.create_line(self.prex, self.prey, event.x, event.y,
                                        fill = self.color.get(),
                                        width = self.width.get(),tag="green")
                self.greenx.append(self.sx)
                self.greeny.append(self.sy)

            self.prex=event.x
            self.prey=event.y
    # ドラッグ
    """
    def on_dragged(self, event):
        self.canvas.create_line(self.sx, self.sy, event.x, event.y,
                                fill = self.color.get(),
                                width = self.width.get())
        self.sx = event.x
        self.sy = event.y

        print(self.sx)

    """
    # ウィンドウを作る
    def create_window(self):
        window = tkinter.Tk()


        self.canvas = tkinter.Canvas(window, background = "white",
                                     width = 600, height = 600)

        self.canvas.pack()


        quit_button = tkinter.Button(window, text = "終了",
                                     command = window.quit)
        quit_button.pack(side = tkinter.RIGHT)

        calc_button = tkinter.Button(window, text = "計算",command=self.DTW)
        calc_button.pack(side = tkinter.RIGHT)


        #self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<ButtonPress-1>", self.on_pressed)

        # 色を選ぶ
        COLORS = ["red", "green"]
        self.color = tkinter.StringVar()                    
        self.color.set(COLORS[1])                             
        b = tkinter.OptionMenu(window, self.color, *COLORS) 
        b.pack(side = tkinter.LEFT)

        self.width = tkinter.Scale(window, from_ = 1, to = 15,
                                   orient = tkinter.HORIZONTAL)
        self.width.set(5)
        self.width.pack(side = tkinter.LEFT)
        
        return window;
            
    def run(self):
        self.window.mainloop()

    def doubleerror(self,a,b):
        return (a-b)**2

    def disterror(self,ansx, ansy, gpsx, gpsy):
        return ((ansx - gpsx) ** 2 + (ansy - gpsy) ** 2) ** 0.5

    def first(self,x):
        return x[0]

    def second(self,x):
        return x[1]

    def calc_dtw(self,ansx, ansy, gpsx, gpsy):
        S = len(ansx)
        T = len(gpsx)

        m = [[(0, (0, 0)) for j in range(T)] for i in range(S)]
        m[0][0] = (self.disterror(ansx[0], ansy[0], gpsx[0], gpsy[0]), (-1, -1))
        for i in range(1, S):
            m[i][0] = (m[i - 1][0][0] + self.disterror(ansx[i], ansy[i], gpsx[0], gpsy[0]), (i - 1, 0))
        for j in range(1, T):
            m[0][j] = (m[0][j - 1][0] + self.disterror(ansx[0], ansy[0], gpsx[j], gpsy[j]), (0, j - 1))
        for i in range(1, S):

            for j in range(1, T):
                # print(i,j)

                # for j in range(1,T):
                minimum, index = self.minVal(m[i - 1][j], m[i][j - 1], m[i - 1][j - 1])
                indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
                m[i][j] = (self.first(minimum) + self.disterror(ansx[i], ansy[i], gpsx[j], gpsy[j]), indexes[index])
        return m



    def minVal(self,v1, v2, v3):
        if self.first(v1) <= min(self.first(v2), self.first(v3)):
            return v1, 0
        elif self.first(v2) <= self.first(v3):
            return v2, 1
        else:
            return v3, 2

    def backward(self,m):
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

    def plot_path(self,path, ansx, ansy, gpsx, gpsy, m):

        plt.figure()
        list_d = [[t[0] for t in row] for row in m]
        # ax2.pcolor(list_d, cmap=plt.cm.Blues)
        for i in range(len(path)):
            plt.scatter(path[i, 1], 600-path[i, 0], s=1, color="Blue")

        # ax1.plot(A, range(len(A)),color="Black")
        # ax1.invert_xaxis()
        # ax4.plot(B,color="Red")
        plt.savefig("pic/DTW/DTW2")
        plt.show()
        plt.close()

        plt.figure()

        ax = plt.subplot()
        ax.set_ylim([0, 600])
        ax.set_xlim([0, 600])
        ax.set_aspect('equal')
        for line in path:
            plt.plot([gpsx[line[1]], ansx[line[0]]], [600-gpsy[line[1]], 600-ansy[line[0]]], linewidth=0.8, c="gray")

        ansy=list(map(lambda x:x*-1+600,ansy))
        gpsy=list(map(lambda x:x*-1+600,gpsy))

        plt.plot(ansx, ansy, color="Red")
        plt.plot(gpsx, gpsy, color="Green")

        ax.annotate("s", (ansx[0], ansy[0]), color="Blue")
        ax.annotate("e", (ansx[-1], ansy[-1]), color="Blue")

        ax.annotate("s", (gpsx[0], gpsy[0]), color="Blue")
        ax.annotate("e", (gpsx[-1], gpsy[-1]), color="Blue")

        plt.savefig("pic/DTW/DTW")

        return

    def DTW(self):

        ansx=self.redx
        ansy=self.redy
        gpsx=self.greenx
        gpsy=self.greeny

        # lossx = (calc_dtw(ansx, gpsx)[-1][-1][0]/len(ansx))**0.5
        # lossy = (calc_dtw(ansy, gpsy)[-1][-1][0]/len(ansy))**0.5

        # print("x",lossx)
        # print("y",lossy)

        m = self.calc_dtw(ansx, ansy, gpsx, gpsy)
        path = self.backward(m)
        self.plot_path(path, ansx, ansy, gpsx, gpsy, m)

        return path

    def __init__(self):
        self.window = self.create_window();  # 呼び出すときはself. + メソッド名

# 開始   
Scribble().run()
