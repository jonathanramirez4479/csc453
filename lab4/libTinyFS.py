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
    ret = open_disk(filename=filename, n_bytes=n_bytes)

    if ret != DiskErrorCodes.SUCCESS:
        return ret

    disk = open(filename, "rb+")

    super_block = SuperBlock(num_of_blocks=NUM_OF_BLOCKS)

    magic_num_bytes = super_block.get_magic_number().to_bytes()
    root_dir_block = super_block.get_root_dir_block().to_bytes()
    bitmap_vector = super_block.get_bitmap_vector_as_number().to_bytes()

    data_to_write = magic_num_bytes + root_dir_block + bitmap_vector

    ret = write_block(disk=disk, block_num=0, block_data=bytearray(data_to_write))
    if ret != DiskErrorCodes.SUCCESS:
        return ret

    for i in range(2, NUM_OF_BLOCKS):
        free_block_indicator = bytearray((FileTypes.FREE).to_bytes())
        ret = write_block(disk=disk, block_num=i, block_data=free_block_indicator)
        if ret != DiskErrorCodes.SUCCESS:
            return ret

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
        print(get_error_message(DiskErrorCodes.DISK_ALREADY_MOUNTED))
        return DiskErrorCodes.DISK_ALREADY_MOUNTED

    # read data from disk and construct Disk obj from it with proper block
    # construction and management
    MOUNTED_DISK_BINARY_IO = open(filename, 'rb+')

    # Superblock first byte
    super_block_data = bytearray(BLOCK_SIZE)
    ret = read_block(disk=MOUNTED_DISK_BINARY_IO, block_num=0, block_data=super_block_data)
    if ret != DiskErrorCodes.SUCCESS:
        return ret

    first_byte = super_block_data[0].to_bytes()

    # verify if the file system is the correct type
    if int(first_byte.hex(), 16) != 0x5A:
        print(get_error_message(DiskErrorCodes.DISK_NOT_AVAILABLE))
        return DiskErrorCodes.DISK_NOT_AVAILABLE

    # update global vars
    DEFAULT_DISK_SIZE = len(MOUNTED_DISK_BINARY_IO.read())  # get disk size
    DEFAULT_DISK_NAME = filename
    NUM_OF_BLOCKS = DEFAULT_DISK_SIZE // BLOCK_SIZE

    MOUNTED_DISK = Disk(disk_size=DEFAULT_DISK_SIZE, num_of_blocks=NUM_OF_BLOCKS, block_size=BLOCK_SIZE)
    MOUNTED_DISK.mount_disk(disk=MOUNTED_DISK_BINARY_IO)

    print(f"disk after mounting: {MOUNTED_DISK.get_disk_state()}")
    print(f"bitmap after mounting: {MOUNTED_DISK.get_super_block().get_bitmap_obj()}")
    print(f"root dir inode after mounting: {MOUNTED_DISK.get_root_dir_inode().get_root_inode_data()}")

    return DiskErrorCodes.SUCCESS


def tfs_unmount() -> int:
    """
    tfs_unmount(void) “unmounts” the currently mounted file system. As part of the mount operation
    Use tfs_unmount to cleanly unmount the currently mounted file system. Must return a specified success/error code.
    """
    global MOUNTED_DISK

    MOUNTED_DISK.unmount_disk(disk=MOUNTED_DISK_BINARY_IO)
    MOUNTED_DISK = None

    return DiskErrorCodes.SUCCESS


def tfs_open(name: str) -> int:
    """
    Opens a file for reading and writing on the currently mounted file system. Creates a dynamic resource table entry
    for the file (the structure that tracks open files, the internal file pointer, etc.), and returns a file descriptor
    (integer) that can be used to reference this file while the filesystem is mounted.
    """
    # Look for the file in the root directory inode
    root_inode = MOUNTED_DISK.get_root_dir_inode()
    inode_index = root_inode.get_inode(name)

    if inode_index is None:
        # If file doesn't exist, create a new inode entry
        new_inode = INode()

        # Look for a free block
        block_index = MOUNTED_DISK.get_free_block_index()
        if block_index == DiskErrorCodes.NO_FREE_BLOCK:
            return DiskErrorCodes.NO_FREE_BLOCK

        # Update disk array with the new inode
        MOUNTED_DISK.add_block(block=new_inode, block_index=block_index)

        # Update root directory inode with the new file
        root_inode.add_name_inode(filename=name, inode=block_index)

        # Update the bitmap
        MOUNTED_DISK.get_super_block().get_bitmap_obj().set_bit(block_index)

        inode_index = block_index
    # Create a file descriptor and update the dynamic resource table
    fd = inode_index  # Using the inode index as the file descriptor
    MOUNTED_DISK.add_dynamic_table_entry_fd(fd)

    return fd


def tfs_close(fd: int) -> int:
    # update dynamic table
    MOUNTED_DISK.remove_dynamic_table_entry(fd=fd)


def tfs_write(fd: int, buffer: str, size: int) -> int:
    """
    Writes buffer ‘buffer’ of size ‘size’, which represents an entire file’s contents,
    to the file described by ‘FD’. Sets the file pointer to 0 (the start of the file)
    when done. Returns success/error codes.
    """

    if len(buffer) != size:
        print(get_error_message(DiskErrorCodes.SIZE_MISMATCH))
        return DiskErrorCodes.SIZE_MISMATCH

    root_inode = MOUNTED_DISK.get_root_dir_inode()
    # Check if the file descriptor is valid
    inode_index = root_inode.get_inode_by_fd(fd)
    if inode_index is None:
        print(get_error_message(error_code=DiskErrorCodes.INVALID_FILE_DESCRIPTOR))
        return DiskErrorCodes.INVALID_FILE_DESCRIPTOR

    inode = MOUNTED_DISK.get_disk_state()[inode_index]
    if not isinstance(inode, INode):
        print(get_error_message(DiskErrorCodes.INODE_FAILURE))
        return DiskErrorCodes.INODE_FAILURE

    # Split buffer into block-sized chunks
    blocks_needed = (size + BLOCK_SIZE - 1) // BLOCK_SIZE
    # Check and allocate additional blocks if necessary
    if len(inode.get_data_block_locations()) < blocks_needed:
        additional_blocks_needed = blocks_needed - len(inode.get_data_block_locations())
        for _ in range(additional_blocks_needed):
            free_block_index = MOUNTED_DISK.get_free_block_index()
            if free_block_index == DiskErrorCodes.NO_FREE_BLOCK:
                return DiskErrorCodes.NO_FREE_BLOCK
            # Set Inode data blocks and flip the bits for the bitmap
            inode.add_data_block_location(free_block_index)
            MOUNTED_DISK.add_block(block=DataBlock(), block_index=free_block_index)
            MOUNTED_DISK.get_super_block().get_bitmap_obj().set_bit(free_block_index)

    # Get the current file pointer
    file_pointer = MOUNTED_DISK.get_file_pointer(fd)

    data_blocks = inode.get_data_block_locations()
    buffer_index = 0
    # Write data to allocated blocks
    for block_index in data_blocks:
        if buffer_index >= size:
            break

        data_block = MOUNTED_DISK.get_disk_state()[block_index]
        if not isinstance(data_block, DataBlock):
            data_block = DataBlock()
            MOUNTED_DISK.add_block(block=data_block, block_index=block_index)

        # Calculate the amount of data to write in the current block
        current_pointer_pos = file_pointer % BLOCK_SIZE
        block_data = buffer[buffer_index:buffer_index + BLOCK_SIZE - current_pointer_pos] \
            .encode('utf-8').ljust(root_inode.get_max_name_length(), b'\x00')
        data_block.set_block_data(block_data)

        # Move to the next chunk of data
        data_block.set_block_data(block_data)
        buffer_index += (BLOCK_SIZE - current_pointer_pos)
        file_pointer += len(block_data)

    # Update the file pointer
    MOUNTED_DISK.set_file_pointer(fd=fd, fp=0)

    return DiskErrorCodes.SUCCESS


def tfs_readByte(fileDescriptor: int, buffer: List[str]) -> int:
    """
    /* reads one byte from the file and copies it to ‘buffer’,
    using the current file pointer location and incrementing it by one upon success.
    If the file pointer is already at the end of the file then tfs_readByte()
    should return an error and not increment the file pointer. */
    """
    dynamic_table = MOUNTED_DISK.get_dynamic_table_entries()

    if fileDescriptor not in dynamic_table:
        print(get_error_message(DiskErrorCodes.INVALID_FILE_DESCRIPTOR))
        return DiskErrorCodes.INVALID_FILE_DESCRIPTOR

    inode = MOUNTED_DISK.get_disk_state()[fileDescriptor]
    if not isinstance(inode, INode):
        print(get_error_message(DiskErrorCodes.INODE_FAILURE))
        return DiskErrorCodes.INODE_FAILURE

    file_pointer = MOUNTED_DISK.get_file_pointer(fileDescriptor)

    # Check if the file pointer is at or beyond the file size
    file_size = sum(
        len(MOUNTED_DISK.get_disk_state()[block].get_block_data()) for block in inode.get_data_block_locations())
    if file_pointer >= file_size:
        print(get_error_message(DiskErrorCodes.END_OF_FILE))
        return DiskErrorCodes.END_OF_FILE

    # Calculate the block and the offset within the block
    block_index = file_pointer // BLOCK_SIZE
    block_offset = file_pointer % BLOCK_SIZE

    data_block_index = inode.get_data_block_locations()[block_index]
    data_block = MOUNTED_DISK.get_disk_state()[data_block_index]
    if not isinstance(data_block, DataBlock):
        print(get_error_message(error_code=DiskErrorCodes.READ_FAILURE))
        return DiskErrorCodes.READ_FAILURE

    # Read the byte from the block
    block_data = data_block.get_block_data()
    byte_value = block_data[block_offset]
    byte_value_str = byte_value.to_bytes().decode('utf-8')

    # Copy the byte to the buffer
    buffer.append(byte_value_str)

    MOUNTED_DISK.set_file_pointer(fileDescriptor, file_pointer + 1)

    return DiskErrorCodes.SUCCESS


def tfs_seek(file_descriptor: int, offset: int) -> int:
    """
    /* change the file pointer location to offset (absolute).
    Returns success/error codes.*/
    """
    if file_descriptor <= 0:
        print(get_error_message(DiskErrorCodes.INVALID_FILE_DESCRIPTOR))
        return DiskErrorCodes.INVALID_FILE_DESCRIPTOR

    current_fp = MOUNTED_DISK.get_file_pointer(file_descriptor)

    if current_fp == -1:
        print(get_error_message(DiskErrorCodes.INVALID_FILE_DESCRIPTOR))
        return DiskErrorCodes.INVALID_FILE_DESCRIPTOR

    # Set the new file pointer to the absolute offset
    new_fp = offset
    MOUNTED_DISK.set_file_pointer(file_descriptor, new_fp)

    return DiskErrorCodes.SUCCESS


def tfs_delete(fileDescriptor: int) -> int:
    """
    /* deletes a file and marks its blocks as free on disk. */
    """
    dynamic_table = MOUNTED_DISK.get_dynamic_table_entries()
    if fileDescriptor not in dynamic_table:
        print(get_error_message(error_code=DiskErrorCodes.INVALID_FILE_DESCRIPTOR))
        return DiskErrorCodes.INVALID_FILE_DESCRIPTOR

    inode = MOUNTED_DISK.get_disk_state()[fileDescriptor]
    if not isinstance(inode, INode):
        print(get_error_message(DiskErrorCodes.INODE_FAILURE))
        return DiskErrorCodes.INODE_FAILURE

    # Remove the file from the dynamic resource table
    del dynamic_table[fileDescriptor]

    # Get the root directory inode
    root_dir_inode = MOUNTED_DISK.get_root_dir_inode()

    # Find the filename in the root directory inode
    filename_to_remove = None
    for filename, inode_index in root_dir_inode.get_root_inode_data().items():
        if inode_index == fileDescriptor:
            filename_to_remove = filename
            break

    if filename_to_remove is None:
        print(get_error_message(DiskErrorCodes.FILE_NOT_FOUND))
        return DiskErrorCodes.FILE_NOT_FOUND
    # Remove the file from the root directory inode
    del root_dir_inode.get_root_inode_data()[filename_to_remove]

    # Free its data blocks and inode
    data_block_locations = inode.get_data_block_locations()
    print(f"Data blocks to be deleted in inode {fileDescriptor}: ", data_block_locations)
    for block_index in data_block_locations:
        MOUNTED_DISK.get_disk_state()[block_index] = FileTypes.FREE
        MOUNTED_DISK.get_super_block().get_bitmap_obj().clear_bit(block_index)

    # Free the inode block
    MOUNTED_DISK.get_disk_state()[fileDescriptor] = FileTypes.FREE
    MOUNTED_DISK.get_super_block().get_bitmap_obj().clear_bit(fileDescriptor)

    return DiskErrorCodes.SUCCESS


def tfs_displayFragments() -> int:
    """
    /* This function allows the user to see a map of all blocks with the non-free blocks clearly designated.
     You can return this as a linked list or a bitmap which you can use to display the map with */
    """
    bitmap = MOUNTED_DISK.get_super_block().get_bitmap_obj().__str__()
    bitmap_reversed = bitmap[::-1]
    print(bitmap_reversed)

    return DiskErrorCodes.SUCCESS


def tfs_defrag():
    """
    /* moves blocks such that all free blocks are contiguous at the end of the disk.
    This should be verifiable with the tfs_displayFraments() function */
    """

    disk_state = MOUNTED_DISK.get_disk_state()
    super_block = MOUNTED_DISK.get_super_block()
    bitmap = super_block.get_bitmap_obj()

    occupied_blocks = []
    free_blocks = []

    for block_index in range(2, len(disk_state)):
        if bitmap.get_bit(block_index) == 1:
            occupied_blocks.append(block_index)
        else:
            free_blocks.append(block_index)

    # Move occupied blocks to the start of the disk
    next_free_index = 2

    inode_updates = {}

    for original_index in occupied_blocks:
        if original_index != next_free_index:
            # Move the block
            disk_state[next_free_index] = disk_state[original_index]
            disk_state[original_index] = FileTypes.FREE

            # Update the bitmap
            bitmap.clear_bit(original_index)
            bitmap.set_bit(next_free_index)

            # If the block is an inode, record its new location
            if isinstance(disk_state[next_free_index], INode):
                inode_updates[original_index] = next_free_index

            # Update inode data block locations
            for inode in disk_state:
                if isinstance(inode, INode):
                    data_blocks = inode.get_data_block_locations()
                    for i, block in enumerate(data_blocks):
                        if block == original_index:
                            data_blocks[i] = next_free_index

            next_free_index += 1
        else:
            next_free_index += 1

    # Clear the remaining blocks in the disk and bitmap
    for free_index in range(next_free_index, len(disk_state)):
        disk_state[free_index] = FileTypes.FREE
        bitmap.clear_bit(free_index)

    # Update the root directory inode to reflect any inode changes
    root_dir_inode = MOUNTED_DISK.get_root_dir_inode()
    root_dir_entries = root_dir_inode.get_root_inode_data()

    for filename, inode_block_index in root_dir_entries.items():
        if inode_block_index in inode_updates:
            root_dir_entries[filename] = inode_updates[inode_block_index]

    print("Defragmentation complete.")
    tfs_displayFragments()

def tfs_rename(old_file_name: str, new_file_name: str):
    # check if valid filename
    # go through root_dir_inode
    # if you fine old_file_name, change it to new file name

    root_dir_inode = MOUNTED_DISK.get_root_dir_inode()

    for filename, block_index in root_dir_inode.get_root_inode_data().items():
        if filename == old_file_name:
            del root_dir_inode.get_root_inode_data()[filename]
            root_dir_inode.get_root_inode_data()[new_file_name] = block_index
            return DiskErrorCodes.SUCCESS

    print(get_error_message(DiskErrorCodes.FILE_NOT_FOUND))
    return DiskErrorCodes.FILE_NOT_FOUND


def tfs_readdir():
    print("Disk files:")
    i = 1
    for filename, block_index in MOUNTED_DISK.get_root_dir_inode().get_root_inode_data().items():
        print(f"\t{i}) {filename}")
        i += 1

