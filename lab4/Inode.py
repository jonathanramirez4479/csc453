from libDisk import BLOCK_SIZE

class INode:
    def __init__(self):
        self.__data_locations = [BLOCK_SIZE]
