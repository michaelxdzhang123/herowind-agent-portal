#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import numpy as np


class Cursor:
  """十字准星光标，用于在 Matplotlib 图表中跟随鼠标移动并显示坐标。"""

  def __init__(self, ax):
    """初始化光标对象。

    参数:
        ax (matplotlib.axes.Axes): 要添加光标的坐标轴对象。
    """
    self.ax = ax
    self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
    self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
    # text location in axes coordinates
    self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

  def set_cross_hair_visible(self, visible):
    """设置十字准星及其坐标文本的可见性。

    参数:
        visible (bool): 是否显示十字准星。

    返回:
        bool: 可见性是否发生变化，若变化则需要重绘。
    """
    need_redraw = self.horizontal_line.get_visible() != visible
    self.horizontal_line.set_visible(visible)
    self.vertical_line.set_visible(visible)
    self.text.set_visible(visible)
    return need_redraw

  def on_mouse_move(self, event):
    """鼠标移动事件处理函数，更新十字线位置并显示当前坐标。

    参数:
        event (matplotlib.backend_bases.MouseEvent): 鼠标移动事件对象。
    """
    if not event.inaxes:
      need_redraw = self.set_cross_hair_visible(False)
      if need_redraw:
        self.ax.figure.canvas.draw()
    else:
      self.set_cross_hair_visible(True)
      x, y = event.xdata, event.ydata
      # update the line positions
      self.horizontal_line.set_ydata(y)
      self.vertical_line.set_xdata(x)
      self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
      self.ax.figure.canvas.draw()
