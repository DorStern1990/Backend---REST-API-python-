
class Dict2D:
    def __init__(self):
        self.dict = dict()
        self.index = 0

    def isDictNotEmpty(self):
        return len(self.dict)

    def insert(self, jyson):
        key = self.index
        assert (key not in self.dict)
        x_coor = jyson['x']  # What if not received appropriately?
        y_coor = jyson['y']  # What if not received appropriately?
        self.dict[key] = (x_coor, y_coor)
        self.index = key + 1
        # Once returned, KD-Tree need to be updated
        return key

    def remove(self, key):
        del self.dict[key] # try catch - KeyError if doesn't exist, nothing otherwise
        # Once returned, KD-Tree need to be updated

    def get(self,key):
        return self.dict[key] # None if doesn't exist, point pair if does

    def getAll(self):
        return self.dict.items()
