import os
from typing import BinaryIO, Union

BLOCK_SIZE = 256  # bytes


class DiskErrorCodes:
    SUCCESS = 0  # operation successful
    DISK_NOT_AVAILABLE = -1  # could not open/create/access disk (file)
    READ_FAILURE = -2  # could not read from disk (file)
    WRITE_FAILURE = -3  # could not write to disk (file)
    SEEK_FAILURE = -4  # could not move file seek pointer in disk (file)
    SIZE_MISMATCH = -5  # size not integral to BLOCK_SIZE
    DISK_ALREADY_MOUNTED = -6  # disk is already mounted
    NO_FREE_BLOCK = -7  # no free block to allocate
    INVALID_FILE_DESCRIPTOR = -8  # FD used by user in tfs_write is invalid
    INODE_FAILURE = -9  # Either some kind of allocation or cleanup error on this Inode
    FILE_POINTER_NOT_FOUND = -10  # General error for file pointer handling
    END_OF_FILE = -11  # File pointer has reached end of file and is attempting to go beyond it
    FILE_NOT_FOUND = -12  # File to be deleted is not found based on FD

    ERROR_MESSAGES = {
        SUCCESS: "Success",
        DISK_NOT_AVAILABLE: "Disk not available or hasn't been opened",
        READ_FAILURE: "Failed to read from disk",
        WRITE_FAILURE: "Failed to write to disk",
        SEEK_FAILURE: "Failed to seek the specified block",
        DISK_ALREADY_MOUNTED: "Disk already mounted",
        NO_FREE_BLOCK: "No free block available to allocate",
        INVALID_FILE_DESCRIPTOR: "Invalid file descriptor",
        INODE_FAILURE: "INode failure",
        FILE_POINTER_NOT_FOUND: "File pointer not found",
        END_OF_FILE: "End of file",
        SIZE_MISMATCH: "sizes don't match",
    }


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

        return DiskErrorCodes.SUCCESS

    except OSError as error:
        print(get_error_message(DiskErrorCodes.DISK_NOT_AVAILABLE))
        return DiskErrorCodes.DISK_NOT_AVAILABLE


def read_block(disk: BinaryIO, block_num: int, block_data: bytearray) -> int:
    """
    Reads an entire block of BLOCK_SIZE bytes from the open disk into the block.

    :param disk: The file object that was opened
    :param block_num: The logical block number
    :param block_data: The local buffer to store the disk data
    :return: 0 if successful
    """
    if len(block_data) < BLOCK_SIZE:
        print(get_error_message(DiskErrorCodes.SIZE_MISMATCH))
        return DiskErrorCodes.SIZE_MISMATCH

    if disk is None:
        print(get_error_message(DiskErrorCodes.DISK_NOT_AVAILABLE))
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    byte_offset = block_num * BLOCK_SIZE

    try:
        disk.seek(byte_offset)
    except OSError as e:
        print(get_error_message(DiskErrorCodes.SEEK_FAILURE))
        return DiskErrorCodes.SEEK_FAILURE

    try:
        block_data[:] = disk.read(BLOCK_SIZE)
    except OSError as e:
        print(get_error_message(DiskErrorCodes.READ_FAILURE))
        return DiskErrorCodes.READ_FAILURE

    return DiskErrorCodes.SUCCESS


def write_block(disk: BinaryIO, block_num: int, block_data: bytearray) -> int:
    """
    Writes a block of BLOCK_SIZE bytes from block to logical block number
    b_num from buffer 'block'

    :param disk: The file object that was opened
    :param block_num: The logical block number
    :param block_data: The local buffer to write from into disk
    :return: 0 if successful
    """
    if disk is None:
        print(get_error_message(DiskErrorCodes.DISK_NOT_AVAILABLE))
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    byte_offset = block_num * BLOCK_SIZE
    try:
        disk.seek(byte_offset)
    except OSError as e:
        print(get_error_message(DiskErrorCodes.SEEK_FAILURE))
        return DiskErrorCodes.SEEK_FAILURE

    try:
        disk.write(block_data)
    except OSError as e:
        print(get_error_message(DiskErrorCodes.WRITE_FAILURE))
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
        print(get_error_message(DiskErrorCodes.DISK_NOT_AVAILABLE))
        return DiskErrorCodes.DISK_NOT_AVAILABLE