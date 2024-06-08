from SuperBlock import SuperBlock
from RootDirINode import RootDirINode
from DataBlock import DataBlock
from FileTypes import FileTypes
from INode import INode
from typing import List, Union, BinaryIO

class Disk:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, num_of_blocks: int, block_size: int, disk_size: int):
        # initialized __disk as a block array
        #    [0, 1, 2, ... (DEFAULT_DISK_SIZE // BLOCK_SIZE) - 1]
        self.__disk: List[Union[
            int, SuperBlock, RootDirINode, INode, DataBlock, None
        ]] = [None] * num_of_blocks

        self.__num_of_blocks: int = num_of_blocks
        self.__disk_size: int = disk_size
        self.__block_size: int = block_size
        self.__dynamic_table_entry: dict = {}  # keeps track of open files in (filename, fp) pairs

    def get_disk_state(self):
        return self.__disk

    def get_super_block(self) -> SuperBlock:
        super_block: SuperBlock = self.__disk[0]
        return super_block

    def get_root_dir_inode(self) -> RootDirINode:
        root_dir_block_index: int = self.get_super_block().get_root_dir_block()
        return self.__disk[root_dir_block_index]


    def mount_disk(self, disk: BinaryIO):
        """TODO: correctly read inode and data blocks into self.__disk """

        # set superblock
        disk.seek(2)
        super_block = SuperBlock(num_of_blocks=self.__num_of_blocks)
        bitmap_vector_num = int.from_bytes(disk.read(1), "little")
        super_block.set_bitmap_vector_number(bitmap_vector_num=bitmap_vector_num)

        self.__disk[0] = super_block

        # set root directory inode
        root_dir_inode = RootDirINode(disk_size=self.__disk_size, block_size=self.__block_size)

        disk.seek(self.__block_size) # set to root dir inode block
        while disk.tell() < (self.__block_size * 2) - root_dir_inode.get_entry_size():
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

        self.__disk[1] = root_dir_inode


        for i in range(2, len(self.__disk)):
            disk.seek(i * self.__block_size)  # set to beginning of block
            first_byte = disk.read(1)  # read the first byte of the block (aka the file type)
            first_byte_int = int.from_bytes(first_byte, "little")

            # check if free block
            if first_byte_int == 4:
                self.__disk[i] = FileTypes.FREE


    def unmount_disk(self, disk: BinaryIO):
        """ TODO: correctly read inode and data blocks into _disk """

        # write superblock to disk
        super_block: SuperBlock = self.__disk[0]

        bitmap_vector_bytes = super_block.get_bitmap_obj().get_bitmap_as_number().to_bytes()
        byte_offset = len(super_block.get_magic_number().to_bytes() + super_block.get_root_dir_block().to_bytes())

        disk.seek(byte_offset)

        disk.write(bitmap_vector_bytes)

        # write the root directory inode to disk
        root_dir_inode: RootDirINode = self.get_root_dir_inode()
        root_dir_inode_dict = root_dir_inode.get_root_dir_inode()

        # set fp to root_dir_block + 1 byte (to account for file type byte)
        disk.seek(super_block.get_root_dir_block() * self.__block_size + 1)

        # write name, inode pairs to disk for root directory inode data
        for filename, inode in root_dir_inode_dict.items():

            # check if fp  out of bounds
            if disk.tell() >= (self.__block_size * 2) - inode.get_entry_size():
                break

            filename_bytes = filename.encode('utf-8')
            inode_bytes = inode.to_bytes()

            root_dir_entry = filename_bytes + inode_bytes
            disk.write(root_dir_entry)

        disk.flush()
