from Disk import *
from FileTypes import FileTypes

DEFAULT_DISK_SIZE = 10240  # bytes = 40 blocks; CAN CHANGE TO SUPPORT VARIABLE SIZE
DEFAULT_DISK_NAME = "tinyFSDisk"
NUM_OF_BLOCKS = DEFAULT_DISK_SIZE // BLOCK_SIZE

MOUNTED_DISK_BINARY_IO = None
MOUNTED_DISK = None

class Block:
    def __init__(self):
        self.__data = bytes()

    def set_block_data(self, data: bytes):
        self.__data = data

    def get_block_data(self) -> bytes:
        return self.__data


def tfs_mkfs(filename: str, n_bytes: int) -> int:
    """
    This function opens a disk (creates a file) and initializes the disk
    to have a super block, root directory inode, and free blocks up the
    max number of possible blocks per the disk size

    :param filename: string file name
    :param n_bytes: number of bytes for disk initialization
    :return: succss/error codes
    """
    disk = open_disk(filename=filename, n_bytes=n_bytes)
    if isinstance(disk, int):  # If the returned value is an error code
        return disk  # return error code

    super_block = SuperBlock(num_of_blocks=NUM_OF_BLOCKS)

    magic_num_bytes = super_block.get_magic_number().to_bytes()
    root_dir_block = super_block.get_root_dir_block().to_bytes()
    bitmap_vector = super_block.get_bitmap_vector_as_number().to_bytes()

    data_to_write = magic_num_bytes + root_dir_block + bitmap_vector

    write_block(disk=disk, block_num=0, block_data=bytearray(data_to_write))

    for i in range(2, NUM_OF_BLOCKS):
        free_block_indicator = bytearray((FileTypes.FREE).to_bytes())
        write_block(disk=disk, block_num=i, block_data=free_block_indicator)

    return DiskErrorCodes.SUCCESS


def tfs_mount(filename: str) -> int:
    """
    tfs_mount(char *filename) “mounts” a TinyFS file system located within an emulated libDisk disk called ‘filename’.
    tfs_mount should verify the file system is the correct type. Only one file system may be mounted at a time. Must
    return a specified success/error code.
    """
    global MOUNTED_DISK_BINARY_IO
    global DEFAULT_DISK_SIZE
    global DEFAULT_DISK_NAME
    global MOUNTED_DISK
    global NUM_OF_BLOCKS

    # check if a disk is already mounted
    if MOUNTED_DISK is not None:
        return DiskErrorCodes.DISK_ALREADY_MOUNTED

    # read data from disk and construct Disk obj from it with proper block
    # construction and management
    with open(filename, 'rb') as f:
        # Superblock first byte
        first_byte = f.read(1)

        # verify if the file system is the correct type
        if int(first_byte.hex(), 16) != 0x5A:
            return DiskErrorCodes.DISK_NOT_AVAILABLE

        # update global vars
        f.seek(0)
        DEFAULT_DISK_SIZE = len(f.read())  # get disk size
        DEFAULT_DISK_NAME = filename
        NUM_OF_BLOCKS = DEFAULT_DISK_SIZE // BLOCK_SIZE
        MOUNTED_DISK_BINARY_IO = f

        MOUNTED_DISK = Disk(disk_size=DEFAULT_DISK_SIZE, num_of_blocks=NUM_OF_BLOCKS, block_size=BLOCK_SIZE)
        MOUNTED_DISK.mount_disk(disk=MOUNTED_DISK_BINARY_IO)

        # print(MOUNTED_DISK.get_disk_state())

    return DiskErrorCodes.SUCCESS


def tfs_unmount() -> int:
    """
    tfs_unmount(void) “unmounts” the currently mounted file system. As part of the mount operation
    Use tfs_unmount to cleanly unmount the currently mounted file system. Must return a specified success/error code.
    """
    global MOUNTED_DISK_BINARY_IO
    global MOUNTED_DISK

    MOUNTED_DISK = None
    MOUNTED_DISK_BINARY_IO = None

    return DiskErrorCodes.SUCCESS


def tfs_open(name: str) -> int:
    """
    Opens a file for reading and writing on the currently mounted file system. Creates a dynamic resource table entry
    for the file (the structure that tracks open files, the internal file pointer, etc.), and returns a file descriptor
    (integer) that can be used to reference this file while the filesystem is mounted.
    """

    return 1
