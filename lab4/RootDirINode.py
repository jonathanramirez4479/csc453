class RootDirINode:
    def __init__(self, disk_size, block_size):
        self.__root_inode = {}
        self.__disk_size = disk_size
        self.__block_size = block_size
        self.__root_inode_limit = (disk_size // block_size) - 2

    def get_root_inode_size(self):
        return len(self.__root_inode)

    def get_root_inode(self):
        return self.__root_inode
