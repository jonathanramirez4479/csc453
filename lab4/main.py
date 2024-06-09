from libDisk import *
from TinyFS import *


def main():
    test_disk = tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)
    tfs_mount(filename=DEFAULT_DISK_NAME)

    with open(DEFAULT_DISK_NAME, 'rb') as f:
        first_file_descriptor = tfs_open(name="foo.c")

        write_status = tfs_write(first_file_descriptor, "a" * 257, 257)
        if write_status != DiskErrorCodes.SUCCESS:
            print(f"Write Error: {write_status}")
            return

        # Read each byte from the file
        read_bytes = bytearray()
        for i in range(12):
            buffer = bytearray()
            byte_value = tfs_readByte(first_file_descriptor, buffer)
            if byte_value != DiskErrorCodes.SUCCESS:
                print(f"Read Error at offset {i}: {byte_value}")
                return
            read_bytes.append(buffer[0])

        print(f"Read Bytes: {read_bytes.decode('utf-8')}")

    tfs_unmount()


    #     # test_write_error = tfs_write(0, "hello world!", 9) #FD error
    #     # print(test_write_error) # -8 error code
    #     tfs_open(name="bar.c")
    #
    # tfs_unmount()


if __name__ == "__main__":
    main()
