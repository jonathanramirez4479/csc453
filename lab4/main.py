from libDisk import *
from TinyFS import *
def main():
    test_disk = tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)
    tfs_mount(filename=DEFAULT_DISK_NAME)

    with open(DEFAULT_DISK_NAME, 'rb') as f:
        f.seek(0)
        print(f.read(BLOCK_SIZE))
        print()
        f.seek(BLOCK_SIZE) # Root Dir
        print(f.read(BLOCK_SIZE))
    tfs_open(name="foo.c")

    # tfs_close(2)

    # with open(DEFAULT_DISK_NAME, 'rb') as f:
    #     f.seek(0)
    #     print(f.read(BLOCK_SIZE))
    #     print()

    tfs_unmount()



if __name__ == "__main__":
    main()
