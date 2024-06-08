from libDisk import *
from FileType import *


class DataBlock:
    def __init__(self, fileType=FILE_TYPES.DATA):
        self.__fileType = fileType
        self.__data_array = bytearray(BLOCK_SIZE)
