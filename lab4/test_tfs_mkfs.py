import os
from TinyFS import *


def test_tfs_mkfs():
    # Define test parameters
    test_filename = "test_disk.img"
    disk_size = 10240  # 10240 bytes (40 blocks)

    # Step 1: Create the file system
    result = tfs_mkfs(test_filename, disk_size)
    assert result == DiskErrorCodes.SUCCESS, f"tfs_mkfs failed with error code {result}"

    # Step 2: Check the disk file size
    try:
        with open(test_filename, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            assert size == disk_size, f"Disk size mismatch: expected {disk_size}, got {size}"
    except OSError as e:
        assert False, f"Failed to open disk file: {e}"

    # Step 3: Check the superblock initialization
    with open(test_filename, "rb") as f:
        superblock_data = bytearray(BLOCK_SIZE)
        result = read_block(f, 0, superblock_data)
        assert result == DiskErrorCodes.SUCCESS, f"read_block failed with error code {result}"
        superblock = SuperBlock()
        assert superblock_data[0] == superblock.get_magic_number(), \
            f"Superblock magic number mismatch: expected {superblock.get_magic_number()}, got {superblock_data[0]}"

    # Step 4: Check zero initialization of other blocks
    empty_block = bytearray(BLOCK_SIZE)
    with open(test_filename, "rb") as f:
        for block_num in range(1, disk_size // BLOCK_SIZE):
            block_data = bytearray(BLOCK_SIZE)
            result = read_block(f, block_num, block_data)
            assert result == DiskErrorCodes.SUCCESS, f"read_block failed with error code {result}"
            assert block_data == empty_block, f"Block {block_num} is not zero-initialized"

    # Clean up test file
    os.remove(test_filename)

    print("All tests passed!")


# Run the test function
test_tfs_mkfs()
