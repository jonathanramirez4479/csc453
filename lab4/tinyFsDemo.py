from libDisk import *
from libTinyFS import *


def main():
    tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)

    tfs_mount(filename=DEFAULT_DISK_NAME)

    foo_fd = tfs_open(name="foo.c")

    bar_fd = tfs_open(name="bar.c")

    buffer = "hello world"
    buffer2 = "hello jonathan"
    buffer3 = "hello christian"

    tfs_write(fd=foo_fd, buffer=buffer, size=len(buffer))
    tfs_write(fd=foo_fd, buffer=buffer2, size=len(buffer2))
    tfs_write(fd=bar_fd, buffer=buffer3, size=len(buffer3))
    tfs_write(fd=foo_fd, buffer="a"*257, size=257)
    tfs_write(fd=bar_fd, buffer=buffer, size=len(buffer))

    read_buffer = []
    tfs_readByte(fileDescriptor=foo_fd, buffer=read_buffer)
    tfs_readByte(fileDescriptor=foo_fd, buffer=read_buffer)

    tfs_seek(bar_fd, 6)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)

    tfs_seek(bar_fd, 255)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)

    # tfs_readdir()
    #
    # print(read_buffer)
    #
    # tfs_delete(foo_fd)
    #
    # tfs_displayFragments()
    # tfs_defrag()

    # tfs_rename("bar.c", "foo.c")

    # tfs_delete(bar_fd)

    # tfs_displayFragments()

    # f = open(DEFAULT_DISK_NAME, 'rb')
    # print(len(f.read()))

    tfs_unmount()

    tfs_mount(filename=DEFAULT_DISK_NAME)





    # tfs_displayFragments()
    # first_file_descriptor = tfs_open(name="foo.c")
    # # print(first_file_descriptor)
    # tfs_displayFragments()
    # write_status = tfs_write(first_file_descriptor, "abc" * 256, size=len("abc" * 256))
    # tfs_displayFragments()
    # second_file_descriptor = tfs_open(name="bar.c")
    # tfs_displayFragments()
    # second_write_status = tfs_write(second_file_descriptor, "def" * 512, size=len("def" * 512))
    # tfs_displayFragments()
    # # print(second_file_descriptor)
    # third_file_descriptor = tfs_open(name="wumbo.c")
    # # print(third_file_descriptor)
    # tfs_displayFragments()
    # third_write_status = tfs_write(third_file_descriptor, "ghi" * 1024, size=len("ghi" * 1024))
    # tfs_displayFragments()
    # tfs_delete(6)
    # tfs_displayFragments()
    # tfs_defrag()
    # tfs_displayFragments()
    #
    # if write_status != DiskErrorCodes.SUCCESS:
    #     print(f"Write Error: {write_status}")
    #     return
    # # Read each byte from the file
    # read_bytes = bytearray()
    # for i in range(12):
    #     buffer = bytearray()
    #     byte_value = tfs_readByte(first_file_descriptor, buffer)
    #     if byte_value != DiskErrorCodes.SUCCESS:
    #         print(f"Read Error at offset {i}: {byte_value}")
    #         return
    #     read_bytes.append(buffer[0])
    #
    # print(f"Read Bytes: {read_bytes.decode('utf-8')}")

    # tfs_unmount()


if __name__ == "__main__":
    main()
