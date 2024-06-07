class Bitmap:
    def __init__(self, size):
        self.size = size
        self.bitmap = 0

    def set_bit(self, position):
        if 0 <= position < self.size:
            self.bitmap |= (1 << position)
        else:
            raise IndexError("Bit position out of range.")

    def clear_bit(self, position):
        if 0 <= position < self.size:
            self.bitmap &= ~(1 << position)
        else:
            raise IndexError("Bit position out of range.")

    def get_bit(self, position):
        if 0 <= position < self.size:
            return (self.bitmap >> position) & 1
        else:
            raise IndexError("Bit position out of range.")

    def get_bitmap_as_number(self):
        return self.bitmap

    def set_bitmap(self, bitmap: int):
        self.bitmap = bitmap

    def __str__(self):
        return bin(self.bitmap)[2:].zfill(self.size)
