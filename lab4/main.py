from libDisk import *
from TinyFS import *


def main():
    test_disk = tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)
    tfs_mount(filename=DEFAULT_DISK_NAME)


    tfs_displayFragments()
    first_file_descriptor = tfs_open(name="foo.c")
    # print(first_file_descriptor)
    tfs_displayFragments()
    write_status = tfs_write(first_file_descriptor, "abc" * 256, 256)
    tfs_displayFragments()
    second_file_descriptor = tfs_open(name="bar.c")
    tfs_displayFragments()
    second_write_status = tfs_write(second_file_descriptor, "def" * 1024, 1024)
    tfs_displayFragments()
    # print(second_file_descriptor)
    third_file_descriptor = tfs_open(name="wumbo.c")
    # print(third_file_descriptor)
    tfs_displayFragments()
    third_write_status = tfs_write(third_file_descriptor, "ghi" * 2048, 2048)
    tfs_displayFragments()
    tfs_delete(4)
    tfs_displayFragments()


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
