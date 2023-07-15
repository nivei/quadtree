from __future__ import annotations
from typing import Optional, Union


#from sys import setrecursionlimit
#setrecursionlimit(2000)


class Point:
    def __init__(self, x:float=.0, y:float=.0, user_data:Optional=None) -> Point:
        self.x = x
        self.y = y
        
        self.user_data = user_data


class Rectangle:
    def __init__(self, x:float=.0, y:float=.0, w:int=0, h:int=0) -> Rectangle:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, rect:Rectangle) -> list:
        if rect.x + rect.w > self.x or rect.x < self.x + self.w or rect.y > self.y or rect.y < self.y + self.h:
            return True
        return False

    def get_rect(self) -> list[Union[int, float]]:
        return [self.x, self.y, self.w, self.h]

    def contains(self, point:Point) -> bool:
        if point.x >= self.x and point.x <= self.w + self.x and point.y <= self.h + self.y and point.y >= self.y:
            return True
        return False


class Circle:
    def __init__(self, x:float=.0, y:float=.0, r:int=0) -> Circle:
        self.x = x
        self.y = y

        self.r = r

    def intersects(self, rect:Rectangle) -> bool:
        circle_dist_x = abs(self.x - rect.x)
        circle_dist_y = abs(self.y - rect.y)

        if circle_dist_x > rect.w + self.r: return False
        if circle_dist_y > rect.h + self.r: return False
        if circle_dist_x <= rect.w:         return True
        if circle_dist_y <= rect.h:         return True

        corner_dist_rect = (
            (circle_dist_x - rect.w)**2 +
            (circle_dist_y - rect.h)**2)

        return corner_dist_rect <= self.r**2 

    def contains(self, point:Point) -> bool:
        if (self.x - point.x)**2 + (self.y - point.y)**2 <= self.r**2:
            return True
        return False


class QuadTree:
    def __init__(self, boundary:Rectangle, capacity:int=4) -> QuadTree:
        self.boundary = boundary
        self.capacity = capacity

        self.points = []
        self.quads = []

        self.divided = False

    def query_cr(self, circle:Circle) -> list[Point]:
        found = []
        if not circle.intersects(self.boundary):
            return found
        for point in self.points:
            if circle.contains(point):
                found.append(point)
        if self.divided:
            for quad in self.quads:
                found += quad.query_cr(circle)
        return found

    def query_sq(self, square:Rectangle) -> list[Point]:
        found = []
        if not self.boundary.intersects(square):
            return found
        for point in self.points:
            if square.contains(point):
                found.append(point)
        if self.divided:
            for quad in self.quads:
                found += quad.query_sq(square)
        return found

    def subdivide(self) -> None:
        self.divided = True
        
        width_d2 = self.boundary.w / 2
        height_d2 = self.boundary.h / 2

        self.quads = []
        self.quads.append(QuadTree(Rectangle(self.boundary.x           , self.boundary.y            , width_d2, height_d2), self.capacity))
        self.quads.append(QuadTree(Rectangle(self.boundary.x + width_d2, self.boundary.y            , width_d2, height_d2), self.capacity))
        self.quads.append(QuadTree(Rectangle(self.boundary.x           , self.boundary.y + height_d2, width_d2, height_d2), self.capacity))
        self.quads.append(QuadTree(Rectangle(self.boundary.x + width_d2, self.boundary.y + height_d2, width_d2, height_d2), self.capacity))

    def insert(self, point:Point) -> None:
        if self.boundary.contains(point):
            if len(self.points) < self.capacity:
                self.points.append(point)
            else:
                if not self.divided:
                    self.subdivide()
                for quad in self.quads:
                    quad.insert(point)

                