import os
import random
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from skimage import io,color
import cv2

from matplotlib import pyplot as plt

FROM_PATH = "D:/Dropbox/Single_Worms/344_890_5515.0_x1y1x2y2_926_478_961_513.png"
TO_PATH = "D:/Dropbox/Single_Worms/344_890_5515.0_x1y1x2y2_926_478_961_513_Annotated.png"

class PaintBrush:
    def __init__(self, line, workingMatrix, subplot):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cidpress = line.figure.canvas.mpl_connect('button_press_event', self.click)
        self.cidrelease = line.figure.canvas.mpl_connect("button_release_event", self.release)
        self.cidmove = line.figure.canvas.mpl_connect("motion_notify_event",self.move)
        self.cidleave = line.figure.canvas.mpl_connect("figure_leave_event", self.release)
        self.is_clicked = False
        self.del_clicked = False
        self.matrix = workingMatrix
        self.ax = subplot

    def click(self, event):
        if event.inaxes!=self.line.axes: return
        if event.button == 1:
          self.is_clicked = True
        elif event.button == 3:
          self.del_clicked = True

    def release(self,event):
      self.is_clicked = False
      self.del_clicked = False

    def move(self, event):
      if event.inaxes!=self.line.axes: return
      if self.is_clicked:
        self.change(event.xdata, event.ydata)
      if self.del_clicked:
        self.unchange(event.xdata, event.ydata)

    def change(self, x, y):
      rgb_values = self.matrix[int(y),int(x)]
      if np.all(rgb_values == rgb_values[0]):
        rgb_values[0]+=20

        self.matrix[int(y),int(x)] = rgb_values
        self.ax.imshow(self.matrix)
        plt.draw()

    def unchange(self, x, y):
      rgb_values = self.matrix[int(y),int(x)]
      if not np.all(rgb_values == rgb_values[0]):
        rgb_values[0]-=20
        self.matrix[int(y),int(x)] = rgb_values
        self.ax.imshow(self.matrix)
        plt.draw()
    def getMatrix(self):
      return self.matrix

if __name__ == "__main__":

  fig, ax = plt.subplots(1)

  ax.set_title('click to add points')
  workingMatrix = cv2.imread(FROM_PATH)
  temp = workingMatrix
  ax.imshow(workingMatrix)
  line, = ax.plot([], [], linestyle="none", marker="o", color="r")

  image_editor = PaintBrush(line, workingMatrix, ax)

  plt.show()

  end_img = image_editor.getMatrix()
  print(end_img)

  cv2.imwrite(TO_PATH,end_img)
