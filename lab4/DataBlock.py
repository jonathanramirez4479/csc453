from libDisk import *

class DataBlock:
    def __init__(self):
        self.__data: bytes = bytes(BLOCK_SIZE)

    def set_block_data(self, data: bytes):
        self.__data = data + bytes(BLOCK_SIZE - len(data))

    def get_block_data(self) -> bytes:
        return self.__data