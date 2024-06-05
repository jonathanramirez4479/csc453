from libDisk import *

DEFAULT_DISK_SIZE = 10240  # bytes = 40 blocks
DEFAULT_DISK_NAME = "tinyFSDisk"

class SuperBlock:
    def __init__(self):
        self.__magic_number = 0x5A
        self.__root_dir_inode = {}
        self.__free_block_bit_vector = '0' * (DEFAULT_DISK_SIZE // BLOCK_SIZE)

    def get_magic_number(self):
        return self.__magic_number

    def get_free_block_bit_vector(self):
        return self.__free_block_bit_vector


class INode:
    def __init__(self):
        self.__file_size = 0
        self.__blocks = []

    def get_file_size(self):
        return self.__file_size

class Data:
    def __init__(self):
        self.__data = bytearray()


class Disk:
    def __init__(self):
        self.__disk = [None] * (DEFAULT_DISK_SIZE // BLOCK_SIZE)

    def add_block(self, block):
        if isinstance(block, (SuperBlock, Data, INode)):
            self.__disk.append(block)

    def get_disk_state(self):
        return self.__disk


# TODO: FINISH THIS FUNCTION
def tfs_mkfs(filename : str, n_bytes : int) -> int:
    """
    Makes an empty TinyFS file system of size nBytes on an emulated libDisk disk specified by ‘filename’.
    This function should use the emulated disk library to open the specified file, and upon success,
    format the file to be mountable. This includes initializing all data to 0x00, setting magic numbers,
    initializing and writing the superblock and other metadata, etc. Must return a specified success/error code.
    int tfs_mkfs(char *filename, int nBytes);
    """
    res = open_disk(filename=filename, n_bytes=n_bytes)

    if (res == DiskErrorCodes.DISK_NOT_AVAILABLE):
        return res



    return res