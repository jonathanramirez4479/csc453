import os
from typing import BinaryIO, Union

BLOCK_SIZE = 256


class DiskErrorCodes:
    SUCCESS = 0  # operation successful
    DISK_NOT_AVAILABLE = 1  # could not open/create/access disk (file)
    READ_FAILURE = 2  # could not read from disk (file)
    WRITE_FAILURE = 3  # could not write to disk (file)
    SEEK_FAILURE = 4  # could not move file seek pointer in disk (file)
    SIZE_MISMATCH = 5  # size not integral to BLOCK_SIZE

    ERROR_MESSAGES = {
        SUCCESS: "Success",
        DISK_NOT_AVAILABLE: "Disk not available or hasn't been opened",
        READ_FAILURE: "Failed to read from disk",
        WRITE_FAILURE: "Failed to write to disk",
        SEEK_FAILURE: "Failed to seek the specified block",
    }
class SuperBlock:
    def __init__(self):
        initialized = 0 # bit to keep track if superblock has been initialized or not
        size_of_free_space = 0 # could be free inodes or bytes
        total_num_files = 0
        magic_number = 0x5A
        location_of_root = 0
        list_of_unallocated_blocks = bytearray(BLOCK_SIZE // 8) # bitmap

class INode:
    def __init__(self):
        Inode_num = 0
        location_of_data = 0
        file_size = 0
        allocated_blocks = [BLOCK_SIZE]
class Root_Directory:
    def __init__(self):
        INode_arr = []


def get_error_message(error_code: int) -> str:
    """
    Returns the error message for a given error code.
    :param error_code: The error code.
    :return: String containing the error message.
    """
    return DiskErrorCodes.ERROR_MESSAGES[error_code]


def open_disk(filename: str, n_bytes: int) -> Union[BinaryIO, int]:
    """
    Opens a file and designates the first n_bytes of it as space
    for emulating a disk.

    :param filename: The string name of a file to open/create.
    :param n_bytes: The number of bytes to use as disk space.
    :return: The file object that was opened
    """
    if n_bytes % BLOCK_SIZE != 0:
        return DiskErrorCodes.SIZE_MISMATCH

    try:
        if n_bytes > 0:
            with open(filename, "wb+") as disk_file:
                disk_file.truncate(n_bytes)

            disk_file = open(filename, "rb+")
        else:
            disk_file = open(filename, "rb+")

        return disk_file

    except OSError as error:
        return DiskErrorCodes.DISK_NOT_AVAILABLE


def read_block(disk: BinaryIO, b_num: int, block: bytearray) -> int:
    """
    Reads an entire block of BLOCK_SIZE bytes from the open disk into the block.

    :param disk: The file object that was opened
    :param b_num: The logical block number
    :param block: The local buffer to store the disk data
    :return: 0 if successful
    """
    if len(block) < BLOCK_SIZE:
        return DiskErrorCodes.SIZE_MISMATCH

    if disk is None:
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    byte_offset = b_num * BLOCK_SIZE

    try:
        disk.seek(byte_offset)
    except OSError as e:
        return DiskErrorCodes.SEEK_FAILURE

    try:
        block[:] = disk.read(BLOCK_SIZE)
    except OSError as e:
        return DiskErrorCodes.READ_FAILURE

    return DiskErrorCodes.SUCCESS


def write_block(disk: BinaryIO, b_num: int, block: bytearray) -> int:
    """
    Writes a block of BLOCK_SIZE bytes from block to logical block number
    b_num from buffer 'block'

    :param disk: The file object that was opened
    :param b_num: The logical block number
    :param block: The local buffer to write from into disk
    :return: 0 if successful
    """
    if disk is None:
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    byte_offset = b_num * BLOCK_SIZE
    try:
        disk.seek(byte_offset)
    except OSError as e:
        return DiskErrorCodes.SEEK_FAILURE

    try:
        disk.write(block)
    except OSError as e:
        return DiskErrorCodes.WRITE_FAILURE

    return DiskErrorCodes.SUCCESS


def close_disk(disk: BinaryIO) -> Union[None, int]:
    """
    Takes a file object and closes it.
    :param disk: The file object that was opened
    :return: None
    """
    try:
        disk.close()
    except OSError as e:
        return DiskErrorCodes.DISK_NOT_AVAILABLE

def initialize_file_system():
    # check superblock initialized bit
    # if bit has not been initialized continue
    # create the superblock
    # create root directory
    # preallocate Inodes??
