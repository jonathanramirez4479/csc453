from libDisk import *

class DataBlock:
    def __init__(self):
        self.__data: bytes = bytes(BLOCK_SIZE - 1)

    def set_block_data(self, data: bytes):
        if len(data) < BLOCK_SIZE:
            self.__data = data

    def get_block_data(self) -> bytes:
        return self.__data