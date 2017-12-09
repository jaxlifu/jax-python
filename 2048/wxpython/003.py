#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import wx
from abc import ABCMeta, abstractmethod


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
        pass

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        pass

    def __str__(self):
        return 'x={0},y={1}'.format(self.x, self.y)
        pass

    @staticmethod
    def dist(a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        pass

    def __repr__(self):
        return str(self.xy)

    @property
    def xy(self):
        return(self.x, self.y)
    pass


class Polygon(object):
    __metaclass__ = ABCMeta

    def __init__(self, point_list, **kwargs):
        for point in point_list:
            assert isinstance(point, Point), 'input must be Point type'
        self.points = point_list
        self.points.append(point_list[0])
        self.color = kwargs.get('color', '#000000')
        pass

    def drawPoints(self):
        points_xy = []
        for point in self.points:
            points_xy.append(point.xy)
        print(points_xy)
        return tuple(points_xy)
        pass

    @abstractmethod
    def area(self):
        raise('not implement')
        pass

    def __lt__(self, other):
        assert isinstance(other, Polygon)
        return self.area < other.area
        pass
    pass


class RectAngle(Polygon):
    def __init__(self, startPoint, w, h, **kwargs):
        self._w = w
        self._h = h
        Polygon.__init__(
            self, [startPoint, startPoint + Point(w, 0),
                   startPoint + Point(w, h), startPoint + Point(0, h)],
            **kwargs)
        pass

    def area(self):
        return self._w * self._h
        pass
    pass


class TriAngle(Polygon):
    def __init__(self, point1, point2, point3, **kwargs):
        if (point1.x == point2.x and point2.x == point3.x) or (
                point1.y == point2.y and point2.y == point3.y):
            assert '三个点在同一条直线上,请重试'
        self._w = point1 - point2
        Polygon.__init__(self, [point1, point2, point3], **kwargs)
        pass

    def area(self):
        return
        pass
    pass


class Example(wx.Frame):
    def __init__(self, title, shapes):
        super(Example, self).__init__(
            None, title=title, size=(600, 400))

        self.shapes = shapes
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Center()
        self.Show()
        pass

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        for shape in self.shapes:
            dc.SetPen(wx.Pen(shape.color))
            dc.DrawLines(shape.drawPoints())
        pass

    pass


if __name__ == '__main__':
    app = wx.App()
    prepare_draws = []
    startPoint = Point(50, 60)
    a = RectAngle(startPoint, 100, 80, color='#ff0000')
    prepare_draws.append(a)

    Example('title', shapes=prepare_draws)
    app.MainLoop()
    pass
