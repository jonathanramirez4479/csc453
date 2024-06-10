from libDisk import *
from TinyFS import *


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

    f = open(DEFAULT_DISK_NAME, 'rb')


if __name__ == "__main__":
    main()
