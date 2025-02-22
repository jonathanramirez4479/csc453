from SuperBlock import SuperBlock
from RootDirINode import RootDirINode
from DataBlock import DataBlock
from FileTypes import FileTypes
from Inode import INode
from typing import List, Union, BinaryIO
from libDisk import *


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
        self.__dynamic_table_entry: dict = {}  # keeps track of open files in (fd, fp) pairs. Lets change this to (fd, fp pairs)
        self.__file_descriptor_table: dict = {}  # fd -> block_index

    def get_fd_table(self):
        return self.__file_descriptor_table

    def add_fd_table_entry(self, fd: int, block_index: int) -> None:
        self.__file_descriptor_table[fd] = block_index

    def get_block_index_from_fd(self, fd: int) -> Union[int, None]:
        return self.__file_descriptor_table[fd]

    def remove_fd_table_entry(self, fd: int) -> None:
        del self.__file_descriptor_table[fd]

    def get_disk_state(self):
        return self.__disk

    def add_dynamic_table_entry(self, filename: str):
        self.__dynamic_table_entry[filename] = 0

    def add_dynamic_table_entry_fd(self, fd: int):
        self.__dynamic_table_entry[fd] = 0

    def remove_dynamic_table_entry(self, fd: int):
        for filename, block_index in self.get_root_dir_inode().get_root_inode_data().items():
            if block_index == fd:
                del self.__dynamic_table_entry[filename]

    def get_dynamic_table_entries(self):
        return self.__dynamic_table_entry

    def get_free_block_index(self) -> int:
        for i in range(2, len(self.__disk)):
            if self.__disk[i] == FileTypes.FREE:
                return i

        return DiskErrorCodes.NO_FREE_BLOCK

    def add_block(self, block: Union[INode, DataBlock], block_index: int):
        assert self.__disk[block_index] == FileTypes.FREE
        self.__disk[block_index] = block

    def get_super_block(self) -> SuperBlock:
        super_block: SuperBlock = self.__disk[0]
        return super_block

    def get_root_dir_inode(self) -> RootDirINode:
        root_dir_block_index: int = self.get_super_block().get_root_dir_block()
        return self.__disk[root_dir_block_index]

    def get_file_pointer(self, fd: int) -> int:
        if fd in self.__dynamic_table_entry:
            return self.get_dynamic_table_entries().get(fd)
        return -1  # Or some error code indicating file not found

    def set_file_pointer(self, fd: int, fp: int):
        if fd in self.__dynamic_table_entry:
            self.__dynamic_table_entry[fd] = fp

    def mount_disk(self, disk: BinaryIO):

        # set superblock
        super_block_data = bytearray(BLOCK_SIZE)
        ret = read_block(disk=disk, block_num=0, block_data=super_block_data)
        if ret != DiskErrorCodes.SUCCESS:
            return ret

        bitmap_vector_int = super_block_data[2]

        super_block = SuperBlock(num_of_blocks=self.__num_of_blocks)
        super_block.set_bitmap_vector_number(bitmap_vector_num=bitmap_vector_int)

        self.__disk[0] = super_block

        # # set root directory inode
        root_dir_inode = RootDirINode(disk_size=self.__disk_size, block_size=self.__block_size)

        root_dir_inode_data = bytearray(BLOCK_SIZE)
        ret = read_block(disk=disk, block_num=1, block_data=root_dir_inode_data)
        if ret != DiskErrorCodes.SUCCESS:
            return ret

        for i in range(0, len(root_dir_inode_data) - root_dir_inode.get_entry_size(), root_dir_inode.get_entry_size()):

            empty_file_name = b'\x00' * root_dir_inode.get_max_name_length()

            entry = root_dir_inode_data[i:i + root_dir_inode.get_entry_size()]

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

        # Load all other blocks
        for i in range(2, len(self.__disk)):
            block = bytearray(BLOCK_SIZE)

            ret = read_block(disk=disk, block_num=i, block_data=block)
            if ret != DiskErrorCodes.SUCCESS:
                return ret

            first_byte_int = block[0]

            # Check block type
            if first_byte_int == FileTypes.FREE:
                self.__disk[i] = FileTypes.FREE
            elif first_byte_int == FileTypes.DATA:
                data_block = DataBlock()
                data_block.set_block_data(block)
                self.__disk[i] = data_block
            elif first_byte_int == FileTypes.INODE:
                inode = INode()
                for j in range(0, len(block), 4):
                    block_location = int.from_bytes(block[j:j + 4], 'little')
                    if block_location != 0:
                        inode.add_data_block_location(block_location)

                self.__disk[i] = inode


    def unmount_disk(self, disk: BinaryIO):
        # write superblock to disk
        super_block: SuperBlock = self.__disk[0]
        magic_number_bytes = super_block.get_magic_number().to_bytes()
        root_dir_inode_block_num = super_block.get_root_dir_block().to_bytes()
        bitmap_vector_bytes = super_block.get_bitmap_obj().get_bitmap_as_number().to_bytes(5)
        super_block_data = bytearray(magic_number_bytes + root_dir_inode_block_num + bitmap_vector_bytes)
        write_block(disk=disk, block_num=0, block_data=super_block_data)

        # write the root directory inode to disk
        root_dir_inode: RootDirINode = self.get_root_dir_inode()
        root_dir_inode_dict = root_dir_inode.get_root_dir_inode()

        root_dir_inode_data = bytearray()

        # write name, inode pairs to disk for root directory inode data
        for filename, inode in root_dir_inode_dict.items():
            entry = filename.encode('utf-8').ljust(root_dir_inode.get_max_name_length(), b'\x00')
            entry += inode.to_bytes()
            root_dir_inode_data.extend(entry)

            write_block(disk=disk, block_num=1, block_data=root_dir_inode_data.ljust(BLOCK_SIZE, b'\x00'))

        # Write all other blocks
        for i in range(2, len(self.__disk)):
            block = self.__disk[i]
            block_data = None
            if isinstance(block, DataBlock):
                block_data = bytearray(BLOCK_SIZE)
                block_data[0] = FileTypes.DATA
                block_data[1:] = bytearray(block.get_block_data())
            elif isinstance(block, INode):
                block_data = bytearray(BLOCK_SIZE)
                block_data[0] = FileTypes.INODE
                block_data[1:] = bytearray(block.get_data_block_locations())


            if block_data is not None and block != FileTypes.FREE:
                write_block(disk=disk, block_num=i, block_data=block_data.ljust(BLOCK_SIZE, b'\x00'))
