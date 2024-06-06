import os
from TinyFS import *
from libDisk import *

def test_tfs_mkfs():

    test_filename = "test_disk.img"

    # Create the file system
    result = tfs_mkfs(test_filename, DEFAULT_DISK_SIZE)
    assert result == DiskErrorCodes.SUCCESS, f"tfs_mkfs failed with error code {result}"
    ###TODO: Making a file system seems to work with tfs_mkfs, however once we are outside of the function, the serialized data does not persist
    ### Must figure out why the superblock is reset to all 0's after tfs_mkfs
    # Mount the file system
    mount = tfs_mount(test_filename)
    assert mount == DiskErrorCodes.SUCCESS, f"tfs_mount failed with error code {result}"

    # Verify the superblock initialization
    assert mounted_superblock.get_magic_number() == 0x5A, "Superblock magic number is incorrect"

    root_inode_block = mounted_superblock.get_root_dir_block()
    assert root_inode_block == 1, "Superblock root directory block pointer is incorrect"

    # Open the disk file using the open_disk function
    disk = open_disk(test_filename, DEFAULT_DISK_SIZE)
    assert not isinstance(disk, int), f"Failed to open disk: {get_error_message(disk)}"

    # Read back and print the root directory to verify
    read_disk = bytearray(BLOCK_SIZE)
    result = read_block(disk, 0, read_disk)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result

    print("Reading disk after tfs_mkfs:", read_disk)

    # Check the disk file size
    try:
        disk.seek(0, os.SEEK_END)
        size = disk.tell()
        assert size == DEFAULT_DISK_SIZE, f"Disk size mismatch: expected {DEFAULT_DISK_SIZE}, got {size}"
    except OSError as e:
        assert False, f"Failed to open disk file: {e}"

    # Verify the superblock initialization
    superblock_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, 0, superblock_data)
    assert result == DiskErrorCodes.SUCCESS, f"read_block for superblock failed with error code {result}"
    assert superblock_data[0] == 0x5A, "Superblock magic number is incorrect"

    root_inode_block = int.from_bytes(superblock_data[1:5], 'little')
    assert root_inode_block == 1, "Superblock root directory block pointer is incorrect"

    # Check zero initialization of other blocks
    empty_block = bytearray(BLOCK_SIZE)
    for block_num in range(1, DEFAULT_DISK_SIZE // BLOCK_SIZE):
        block_data = bytearray(BLOCK_SIZE)
        result = read_block(disk, block_num, block_data)
        assert result == DiskErrorCodes.SUCCESS, f"read_block failed with error code {result}"
        assert block_data == empty_block, f"Block {block_num} is not zero-initialized"

    # Test write_block function
    data_to_write = bytearray(b'Hello, World!'.ljust(BLOCK_SIZE, b'\0'))  # Ensure it's the size of a block
    result = write_block(disk, 1, data_to_write)
    assert result == DiskErrorCodes.SUCCESS, f"write_block failed with error code {result}"

    # Verify that the block was written correctly by reading it back
    written_block_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, 1, written_block_data)
    assert result == DiskErrorCodes.SUCCESS, f"read_block failed with error code {result}"
    assert written_block_data == data_to_write, "Written block data does not match the data written"

    # Close the disk file
    result = close_disk(disk)
    assert result is None, f"Failed to close disk: {get_error_message(result)}"

    # Clean up test file
    os.remove(test_filename)

    print("All tests passed!")


# Run the test function
test_tfs_mkfs()
