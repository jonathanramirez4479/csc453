from libDisk import *
from TinyFS import *


def main():
    test_disk = tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)
    tfs_mount(filename=DEFAULT_DISK_NAME)

    with open(DEFAULT_DISK_NAME, 'rb') as f:
        # f.seek(0)
        # print(f.read(BLOCK_SIZE)) # superblock
        # print()
        # f.seek(BLOCK_SIZE) # Root Dir
        # print(f.read(BLOCK_SIZE))
        first_file_descriptor = tfs_open(name="foo.c")
        print("fd for foo.c", first_file_descriptor)

        block = tfs_write(2, "hello world!", 9) # sizemissmatch error in read?
        # read = read_block(f, 3, bytearray(block))
        # print(read)
        # test_write_error = tfs_write(0, "hello world!", 9) #FD error
        # print(test_write_error) # -8 error code
        tfs_open(name="bar.c")

    # tfs_close(2)

    # with open(DEFAULT_DISK_NAME, 'rb') as f:
    #     f.seek(0)
    #     print(f.read(BLOCK_SIZE))
    #     print()

    tfs_unmount()


if __name__ == "__main__":
    main()
