from scipy.spatial import KDTree
import math

class Tree2D:

    def __init__(self, point):
        self.tree = KDTree(point)

    def update(self, points):
        self.tree = KDTree(points)

    def search(self, x0, y0, width, height):
        center = [x0+0.5*width, y0+0.5*height]
        radius = 0.5*(math.sqrt(width ** 2 + height ** 2))
        points_in_radius = list(self.tree.query_ball_point(center, radius))
        return points_in_radius
