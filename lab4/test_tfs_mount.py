import os
from libTinyFS import *

def test_tfs_mount():
    test_filename = "testDisk"

    # Create and format a new file system
    result = tfs_mkfs(test_filename, DEFAULT_DISK_SIZE)
    assert result == DiskErrorCodes.SUCCESS, f"tfs_mkfs failed with error code {result}"

    # Mount the file system
    result = tfs_mount(test_filename)
    assert result == DiskErrorCodes.SUCCESS, f"tfs_mount failed with error code {result}"

    # Verify that the superblock is correct
    global mounted_superblock
    assert mounted_superblock is not None, "Superblock should be initialized"
    assert mounted_superblock.get_magic_number() == 0x5A, "Magic number is incorrect"

    # Verify that the root directory is initialized
    global mounted_root_directory
    assert mounted_root_directory is not None, "Root directory should be initialized"
    assert isinstance(mounted_root_directory, RootDirectory), "Root directory is not of correct type"

    # Unmount the file system
    result = tfs_unmount()
    assert result == DiskErrorCodes.SUCCESS, f"tfs_unmount failed with error code {result}"

    # Verify that the file system is unmounted
    assert mounted_disk is None, "Disk should be unmounted"
    assert mounted_superblock is None, "Superblock should be reset"
    assert mounted_root_directory is None, "Root directory should be reset"

    # Close the disk file
    result = close_disk(disk)
    assert result is None, f"Failed to close disk: {get_error_message(result)}"
    # Clean up test file
    os.remove(test_filename)
    print("All tests passed.")


# Run the test
test_tfs_mount()