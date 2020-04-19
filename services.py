from PointsDict import Dict2D
from PointsTree import Tree2D


class Services:
    def __init__(self):
        self.pointsDictionary = Dict2D()
        self.pointsTree = Tree2D([(0, 0)])
        self.original = dict()

    def insert(self, json):
        # Inserting a new point, 1st to dictionary
        key = self.pointsDictionary.insert(json)
        # Get all points from points' dictionary as array
        # Recreate tree
        self.original_tree_update_helper()
        return key

    def remove(self, key):
        self.pointsDictionary.remove(key)
        if self.pointsDictionary.isDictNotEmpty():
            self.original_tree_update_helper()

    def get(self, key):
        point = self.pointsDictionary.get(key)
        return point

    def search(self, json):
        if self.pointsDictionary.isDictNotEmpty():
            x_coor = json['x']  # What if not received appropriately?
            y_coor = json['y']  # What if not received appropriately?
            rectangle_width = json['width']  # What if not received appropriately?
            rectangle_height = json['height']  # What if not received appropriately?
            points_in_radius = self.pointsTree.search(x_coor, y_coor, rectangle_width, rectangle_height)  # What if no points in rectangle?
            points_in_rectangle = self.getAllInRectangle(points_in_radius, x_coor, y_coor, rectangle_width, rectangle_height)
            result = points_in_rectangle
        else:
            result = []
        return result

    def original_tree_update_helper(self):
        dict_items = self.pointsDictionary.getAll()
        dict_keys = [point[0] for point in dict_items]
        dict_values = [point[1] for point in dict_items]
        points = [point for point in dict_values]
        keys = [key for key in dict_keys]
        for i in range(0, len(points)):
            self.original[i] = keys[i]
        self.pointsTree.update(points)

    def getAllInRectangle(self, points_in_radius, x0, y0, width, height):
        return [tuple(self.get(self.original[key])) for key in points_in_radius if (x0+width >= self.get(self.original[key])[0] >= x0 and y0+height >= self.get(self.original[key])[1] >= y0)]
