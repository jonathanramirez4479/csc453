from SuperBlock import *
from typing import BinaryIO
from RootDirINode import *

class Disk:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, num_of_blocks, block_size, disk_size):
        # initialized __disk as a block array
        #    [0, 1, 2, ... (DEFAULT_DISK_SIZE // BLOCK_SIZE) - 1]
        self.__disk = [None] * num_of_blocks
        self.__num_of_blocks = num_of_blocks
        self.__disk_size = disk_size
        self.__block_size = block_size

    def get_disk_state(self):
        return self.__disk

    def mount_disk(self, disk: BinaryIO):
        # set superblock
        disk.seek(2)
        super_block = SuperBlock(num_of_blocks=self.__num_of_blocks)
        bitmap_vector_num = int.from_bytes(disk.read(1), "little")
        super_block.set_bitmap_vector_number(bitmap_vector_num=bitmap_vector_num)

        self.__disk[0] = super_block
        self.__disk[1] = RootDirINode(disk_size=self.__disk_size, block_size=self.__block_size)
        # set rest of data