from PIL import Image
from uuid import uuid4


def dhash(image, hash_size=16):
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)

    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)


def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


class MemeImage:
    name = None
    ext = None
    image = None
    hash = None
    src = None
    size = None
    src_url = None

    def __init__(self, image, src, src_url, nxt=None):
        self.image = Image.open(image)
        self.name = uuid4()
        self.nxt = nxt
        self.ext = self.image.format.lower()
        self.src = src
        self.src_url = src_url

        self._generate_hash()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_image()

    def _generate_hash(self):
        self.hash = dhash(self.image)

    def close_image(self):
        self.image.close()

    def hamming_distance(self, hsh):
        if not self.hash:
            self._generate_hash()

        return hamming_distance(self.hash, hsh)
