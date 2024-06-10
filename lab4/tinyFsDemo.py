from libDisk import *
from libTinyFS import *


def main():
    tfs_mkfs(filename=DEFAULT_DISK_NAME, n_bytes=DEFAULT_DISK_SIZE)

    tfs_mount(filename=DEFAULT_DISK_NAME)

    foo_fd = tfs_open(name="foo.c")

    bar_fd = tfs_open(name="bar.c")

    wumbo_fd = tfs_open(name="wumbo.c")

    tfs_readdir()

    buffer = "hello world"
    buffer2 = "hello jonathan"
    buffer3 = "hello christian"

    tfs_write(fd=foo_fd, buffer=buffer, size=len(buffer))
    tfs_write(fd=foo_fd, buffer=buffer2, size=len(buffer2))
    tfs_write(fd=bar_fd, buffer=buffer3, size=len(buffer3))
    tfs_write(fd=foo_fd, buffer="a"*257, size=257)
    tfs_write(fd=bar_fd, buffer=buffer, size=len(buffer))
    tfs_write(fd=wumbo_fd, buffer=buffer, size=len(buffer))

    read_buffer = []
    tfs_readByte(fileDescriptor=foo_fd, buffer=read_buffer)
    tfs_readByte(fileDescriptor=foo_fd, buffer=read_buffer)

    tfs_seek(bar_fd, 6)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)

    tfs_seek(bar_fd, 255)
    tfs_readByte(fileDescriptor=bar_fd, buffer=read_buffer)

    tfs_readdir()

    print(read_buffer)

    tfs_delete(bar_fd)
    tfs_displayFragments()

    tfs_defrag()

    tfs_readByte(fileDescriptor=foo_fd, buffer=read_buffer)
    print(read_buffer)

    tfs_readByte(fileDescriptor=wumbo_fd, buffer=read_buffer)
    print(read_buffer)

    tfs_rename("wumbo.c", "bar.c")

    tfs_readdir()

    tfs_readByte(fileDescriptor=wumbo_fd, buffer=read_buffer)

    print(read_buffer)

    tfs_close(wumbo_fd)

    tfs_displayFragments()

    tfs_unmount()

    tfs_mount(filename=DEFAULT_DISK_NAME)


if __name__ == "__main__":
    main()
