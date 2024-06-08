INODE_SIZE = 1
MAX_NAME_LENGTH = 8
ENTRY_SIZE = MAX_NAME_LENGTH + INODE_SIZE

class RootDirINode:
    def __init__(self, disk_size, block_size):
        self.__root_inode: dict = {}
        self.__disk_size: int = disk_size
        self.__block_size: int = block_size
        self.__root_inode_limit: int = (disk_size // block_size) - 1
        self.__inode_size: int = INODE_SIZE
        self.__max_name_length: int = MAX_NAME_LENGTH
        self.__entry_size: int = ENTRY_SIZE

    def get_root_inode_size(self):
        return len(self.__root_inode)

    def get_root_inode(self):
        return self.__root_inode

    def add_name_inode(self, filename: str, inode: int):
        if filename not in self.__root_inode and inode < self.__root_inode_limit:
            self.__root_inode[filename] = inode

    def get_inode(self, filename: str):
        return self.__root_inode[filename]

    def get_inode_size(self):
        return self.__inode_size

    def get_max_name_length(self):
        return self.__max_name_length

    def get_entry_size(self):
        return self.__entry_size

    def get_root_dir_inode(self):
        return self.__root_inode
