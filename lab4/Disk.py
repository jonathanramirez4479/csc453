from SuperBlock import *
from RootDirINode import *
from DataBlock import *
from FileTypes import FileTypes

class Disk:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, num_of_blocks, block_size, disk_size):
        # initialized __disk as a block array
        #    [0, 1, 2, ... (DEFAULT_DISK_SIZE // BLOCK_SIZE) - 1]
        self.__disk = [None] * num_of_blocks
        self.__num_of_blocks = num_of_blocks
        self.__disk_size = disk_size
        self.__block_size = block_size

    def get_disk_state(self):
        return self.__disk

    def mount_disk(self, disk: BinaryIO):
        # set superblock
        disk.seek(2)
        super_block = SuperBlock(num_of_blocks=self.__num_of_blocks)
        bitmap_vector_num = int.from_bytes(disk.read(1), "little")
        super_block.set_bitmap_vector_number(bitmap_vector_num=bitmap_vector_num)

        self.__disk[0] = super_block

        # set root directory inode
        root_dir_inode = RootDirINode(disk_size=self.__disk_size, block_size=self.__block_size)

        disk.seek(BLOCK_SIZE) # set to root dir inode block
        while disk.tell() < (BLOCK_SIZE * 2) - root_dir_inode.get_entry_size():
            empty_file_name = b'\x00\x00\x00\x00\x00\x00\x00\x00'

            entry = disk.read(root_dir_inode.get_entry_size())

            filename = entry[:root_dir_inode.get_max_name_length()]

            # check if the entry is empty
            if filename == empty_file_name:
                continue

            filename = filename.decode('utf-8')

            inode = entry[root_dir_inode.get_max_name_length():]
            inode = int.from_bytes(inode)

            # add name, inode pair
            root_dir_inode.add_name_inode(filename=filename, inode=inode)

        ### TODO: get blocks according to the disk on file
        # set rest of data as free blocks
        for i in range(2, len(self.__disk)):
            self.__disk[i] = FileTypes.FREE