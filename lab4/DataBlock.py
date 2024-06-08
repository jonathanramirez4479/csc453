from libDisk import *

class DataBlock:
    def __init__(self):
        self.__data: bytes = bytes()

    def set_block_data(self, data: bytes):
        self.__data = data

    def get_block_data(self) -> bytes:
        return self.__data