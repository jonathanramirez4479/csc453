from Disk import *
from FileTypes import FileTypes
from Inode import INode
from libDisk import *

DEFAULT_DISK_SIZE = 10240  # bytes = 40 blocks; CAN CHANGE TO SUPPORT VARIABLE SIZE
DEFAULT_DISK_NAME = "tinyFSDisk"
NUM_OF_BLOCKS = DEFAULT_DISK_SIZE // BLOCK_SIZE

MOUNTED_DISK_BINARY_IO: Union[BinaryIO, None] = None
MOUNTED_DISK: Union[Disk, None] = None


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
    global DEFAULT_DISK_SIZE
    global DEFAULT_DISK_NAME
    global MOUNTED_DISK
    global NUM_OF_BLOCKS
    global MOUNTED_DISK_BINARY_IO


    # check if a disk is already mounted
    if MOUNTED_DISK is not None:
        return DiskErrorCodes.DISK_ALREADY_MOUNTED

    # read data from disk and construct Disk obj from it with proper block
    # construction and management
    MOUNTED_DISK_BINARY_IO = open(filename, 'rb+')
    # Superblock first byte
    first_byte = MOUNTED_DISK_BINARY_IO.read(1)

    # verify if the file system is the correct type
    if int(first_byte.hex(), 16) != 0x5A:
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    # update global vars
    MOUNTED_DISK_BINARY_IO.seek(0)
    DEFAULT_DISK_SIZE = len(MOUNTED_DISK_BINARY_IO.read())  # get disk size
    DEFAULT_DISK_NAME = filename
    NUM_OF_BLOCKS = DEFAULT_DISK_SIZE // BLOCK_SIZE

    MOUNTED_DISK = Disk(disk_size=DEFAULT_DISK_SIZE, num_of_blocks=NUM_OF_BLOCKS, block_size=BLOCK_SIZE)
    MOUNTED_DISK.mount_disk(disk=MOUNTED_DISK_BINARY_IO)

    return DiskErrorCodes.SUCCESS


def tfs_unmount() -> int:
    """
    tfs_unmount(void) “unmounts” the currently mounted file system. As part of the mount operation
    Use tfs_unmount to cleanly unmount the currently mounted file system. Must return a specified success/error code.
    """
    MOUNTED_DISK.unmount_disk(disk=MOUNTED_DISK_BINARY_IO)

    return DiskErrorCodes.SUCCESS


def tfs_open(name: str) -> int:
    """
    Opens a file for reading and writing on the currently mounted file system. Creates a dynamic resource table entry
    for the file (the structure that tracks open files, the internal file pointer, etc.), and returns a file descriptor
    (integer) that can be used to reference this file while the filesystem is mounted.
    """

    # create inode entry
    # add entry to dynamic table entry

    new_inode = INode()

    # look for free block
    block_index = MOUNTED_DISK.get_free_block_index()
    if block_index == DiskErrorCodes.NO_FREE_BLOCK:
        return DiskErrorCodes.NO_FREE_BLOCK

    # update disk array
    MOUNTED_DISK.add_block(block=new_inode, block_index=block_index)

    # update root dir inode
    MOUNTED_DISK.get_root_dir_inode().add_name_inode(filename=name, inode=block_index)

    # update dynamic table
    MOUNTED_DISK.add_dynamic_table_entry(filename=name)

    # update bitmap
    MOUNTED_DISK.get_super_block().get_bitmap_obj().set_bit(block_index)

    return block_index


def tfs_close(fd: int) -> int:
    # update dynamic table
    MOUNTED_DISK.remove_dynamic_table_entry(fd=fd)


# def tfs_write(fd: int, buffer: str, size: int) -> int:
