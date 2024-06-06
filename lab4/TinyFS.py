from libDisk import *

DEFAULT_DISK_SIZE = 10240  # bytes = 40 blocks
DEFAULT_DISK_NAME = "tinyFSDisk"

mounted_disk = None
mounted_superblock = None
mounted_root_directory = None


class SuperBlock:
    def __init__(self, root_dir_block = 1):
        self.__magic_number = 0x5A
        self.__root_dir_block = root_dir_block
        self.__free_block_bit_vector = b'0' * (DEFAULT_DISK_SIZE // BLOCK_SIZE)

    def get_magic_number(self):
        return self.__magic_number

    def get_free_block_bit_vector(self):
        return self.__free_block_bit_vector

    def serialize(self) -> bytearray:
        superblock_data = bytearray(BLOCK_SIZE)
        superblock_data[0] = self.get_magic_number()
        superblock_data[1:5] = self.__root_dir_block.to_bytes(4, 'little')
        superblock_data[5:] = self.__free_block_bit_vector
        return superblock_data

    @staticmethod
    def deserialize(data: bytearray) -> 'SuperBlock':
        magic_number = data[0]
        if magic_number != 0x5A:
            raise ValueError("Invalid magic number")
        root_inode_block = int.from_bytes(data[1:5], 'little')
        free_block_bit_vector = data[5:]
        sb = SuperBlock()
        sb.free_block_bit_vector = free_block_bit_vector
        return sb


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
        data = bytearray(BLOCK_SIZE)
        for entry in self.entries:
            data += entry.serialize()
        return data.ljust(BLOCK_SIZE, b'\0')

    @staticmethod
    def deserialize(data: bytearray) -> 'RootDirectory':
        rd = RootDirectory()
        offset = 0
        while offset < len(data):
            name = data[offset:offset + 8].rstrip('\0')
            inode_number = struct.unpack('<I', data[offset + 8:offset + 12])[0]
            if name:
                rd.add_entry(name, inode_number)
            offset += 12
        return rd


class RootDirectoryEntry:
    def __init__(self, name: str, inode_number: int):
        self.name = name
        self.inode_number = inode_number

    def serialize(self) -> bytearray:
        name_bytes = self.name.ljust(8, b'\0')
        inode_number_bytes = struct.pack('<I', self.inode_number)
        return name_bytes + inode_number_bytes


class INode:
    def __init__(self, inode_number: int):
        self.inode_number = inode_number
        self.file_size = 0
        self.blocks = []

    def get_file_size(self):
        return self.file_size

    def add_block(self, block_number: int):
        self.blocks.append(block_number)


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

    """
    # Read back and print the superblock to verify
        read_superblock_data = bytearray(BLOCK_SIZE)
        result = read_block(disk, 0, read_superblock_data)
        if result != DiskErrorCodes.SUCCESS:
            close_disk(disk)
            return result
    print("Superblock after writing:", read_superblock_data)
    """

    # Initialize the root directory
    root_directory = RootDirectory().serialize()
    result = write_block(disk, 1, root_directory)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result

    """
    # Read back and print the root directory to verify
    read_root_directory_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, 1, read_root_directory_data)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result
    print("Root directory after writing:", read_root_directory_data)
    """

    close_disk(disk)
    return DiskErrorCodes.SUCCESS


def tfs_mount(filename: str) -> int:
    global mounted_disk, mounted_superblock, mounted_root_directory

    if mounted_disk is not None:
        print("Error: A filesystem is already mounted.")
        return DiskErrorCodes.FAILURE

    disk = open_disk(filename, DEFAULT_DISK_SIZE)
    if isinstance(disk, int):  # If the returned value is an error code
        return disk

    # Read the superblock
    superblock_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, 0, superblock_data)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result
    print("superblock from mount: ", superblock_data)

    try:
        superblock = SuperBlock.deserialize(superblock_data)
    except ValueError as e:
        print(e)
        close_disk(disk)
        return DiskErrorCodes.INVALID_FILESYSTEM

    # Read the root directory inode
    root_inode_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, superblock.root_inode_block, root_inode_data)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result

    # Read the root directory data block
    root_directory_data = bytearray(BLOCK_SIZE)
    result = read_block(disk, struct.unpack('<I', root_inode_data[4:8])[0], root_directory_data)
    if result != DiskErrorCodes.SUCCESS:
        close_disk(disk)
        return result

    mounted_disk = disk
    mounted_superblock = superblock
    mounted_root_directory = RootDirectory.deserialize(root_directory_data)

    return DiskErrorCodes.SUCCESS


def tfs_unmount() -> int:
    global mounted_disk, mounted_superblock, mounted_root_directory

    if mounted_disk is None:
        print("Error: No filesystem is currently mounted.")
        return DiskErrorCodes.FAILURE

    # Perform any necessary cleanup here

    close_disk(mounted_disk)
    mounted_disk = None
    mounted_superblock = None
    mounted_root_directory = None

    return DiskErrorCodes.SUCCESS
