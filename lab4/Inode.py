from FileType import *
from libDisk import BLOCK_SIZE


class Inode:
    def __init__(self, fileType=FILE_TYPES.INODE):
        self.__fileType = fileType
        self.__data_locations = [BLOCK_SIZE]
