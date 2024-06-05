from libDisk import *


def main():
    buffer = bytearray(BLOCK_SIZE)

    for i in range(BLOCK_SIZE):
        buffer[i] = i % 256

    data_from_disk = bytearray(BLOCK_SIZE)

    disk = None
    result = open_disk(filename="new_file", n_bytes=256)

    if result is int:
        print(get_error_message(result))
        exit()
    else:
        disk = result

    result = write_block(disk=disk, b_num=0, block=buffer)
    if result != DiskErrorCodes.SUCCESS:
        print(get_error_message(result))

    result = read_block(disk=disk, b_num=0, block=data_from_disk)
    if result != DiskErrorCodes.SUCCESS:
        print(get_error_message(result))

    print(data_from_disk)

def tfs_mkfs(filename : char, nBytes : byte) -> int:
    """
    Makes an empty TinyFS file system of size nBytes on an emulated libDisk disk specified by ‘filename’.
    This function should use the emulated disk library to open the specified file, and upon success,
    format the file to be mountable. This includes initializing all data to 0x00, setting magic numbers,
    initializing and writing the superblock and other metadata, etc. Must return a specified success/error code.
    int tfs_mkfs(char *filename, int nBytes);
    """
    return 0
if __name__ == "__main__":
    main()
