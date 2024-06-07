from Bitmap import Bitmap
class SuperBlock:
    def __init__(self, num_of_blocks):
        self.__magic_number = 0x5A
        self.__root_dir_block = 1  # root directory always at the first block
        self.__bitmap_vector = Bitmap(num_of_blocks)
        self.__bitmap_vector.set_bit(0)  # occupied by superblock
        self.__bitmap_vector.set_bit(1)  # occupied by root dir inode

    def get_magic_number(self) -> int:
        return self.__magic_number

    def get_bitmap_vector_as_number(self) -> int:
        return self.__bitmap_vector.get_bitmap_as_number()

    def set_bitmap_vector_number(self, bitmap_vector_num: int):
        self.__bitmap_vector.set_bitmap(bitmap_vector_num)

    def get_root_dir_block(self) -> int:
        return self.__root_dir_block