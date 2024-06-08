from libDisk import *

class DataBlock:
    def __init__(self):
        self.__data_array = bytearray(BLOCK_SIZE)
