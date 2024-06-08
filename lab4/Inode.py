from libDisk import BLOCK_SIZE
from typing import List

class INode:
    def __init__(self):
        self.__data_block_locations: List[int] = []

    def add_data_block_location(self, block_index):
        self.__data_block_locations.append(block_index)

    def get_data_block_locations(self) -> List[int]:
        return self.__data_block_locations
