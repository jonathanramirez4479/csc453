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

    def serialize(self) -> bytearray:
        superblock_data = bytearray(BLOCK_SIZE)
        superblock_data[0] = self.get_magic_number()
        return superblock_data


class INode:
    def __init__(self, inode_number: int):
        self.inode_number = inode_number
        self.file_size = 0
        self.blocks = []

    def get_file_size(self):
        return self.__file_size

    def add_block(self, block_number: int):
        self.blocks.append(block_number)


class RootDirectoryEntry:
    def __init__(self, name: str, inode_number: int):
        self.name = name
        self.inode_number = inode_number


class RootDirectory:
    def __init__(self):
        self.entries = []

    def add_entry(self, name: str, inode_number: int):
        if len(name) <= 8:
            entry = RootDirectoryEntry(name, inode_number)
            self.entries.append(entry)
        else:
            print("Error: Name exceeds maximum length of 8 characters.")

    def serialize(self) -> bytearray:
        data = bytearray()
        for entry in self.entries:
            data += entry.serialize()
        return data[:BLOCK_SIZE]  # Ensure it fits in one block


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


def tfs_mkfs(filename: str, n_bytes: int) -> int:
    """
    Makes an empty TinyFS file system of size nBytes on an emulated libDisk disk specified by ‘filename’.
    This function should use the emulated disk library to open the specified file, and upon success,
    format the file to be mountable. This includes initializing all data to 0x00, setting magic numbers,
    initializing and writing the superblock and other metadata, etc. Must return a specified success/error code.
    int tfs_mkfs(char *filename, int nBytes);
    """

    disk = open_disk(filename=filename, n_bytes=n_bytes)
    if isinstance(disk, int):  # If the returned value is an error code
        return disk

    # Initialize the disk with zeros
    num_blocks = n_bytes // BLOCK_SIZE
    empty_block = bytearray(BLOCK_SIZE)
    for block_num in range(num_blocks):
        result = write_block(disk, block_num, empty_block)
        if result != DiskErrorCodes.SUCCESS:
            close_disk(disk)
            return result

    # Serialize the superblock into a byte array
    superblock = SuperBlock().serialize()

    # Write the superblock to the disk (block 0)
    result = write_block(disk, 0, superblock)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result

    # Initialize the root directory
    root_directory = RootDirectory().serialize()

    close_disk(disk)
    return DiskErrorCodes.SUCCESS