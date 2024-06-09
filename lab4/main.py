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

        write_status = tfs_write(first_file_descriptor, "hello world!", 12)
        if write_status != DiskErrorCodes.SUCCESS:
            print(f"Write Error: {write_status}")
            return
        tfs_seek(2, 0)  # reset file pointer
        # Read each byte from the file
        read_bytes = []
        for i in range(12):  # Length of "hello world!" is 12
            byte_value = tfs_readByte(first_file_descriptor, i)
            if byte_value < 0:
                print(f"Read Error at offset {i}: {byte_value}")
                return
            read_bytes.append(byte_value)

        # Convert read bytes back to string
        read_string = ''.join(chr(b) for b in read_bytes)
        print(f"Read string: {read_string}")

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
