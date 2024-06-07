from libDisk import *
from TinyFS import *
def main():
    disk = tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)

    tfs_mount(DEFAULT_DISK_NAME)




if __name__ == "__main__":
    main()
