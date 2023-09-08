import numpy as np
from PIL import Image


class ImageSteg:
    def __init__(self, image: Image) -> None:
        self.image = image

    def encode_LSB(
        self, data: str, px: int, py: int
    ) -> Image:  # Assume that no. of pixels in self.image is sufficient to encode data
        # (px, py) = starting coordinate for LSB encoding

        pixels = np.asarray(self.image.convert("RGB"))

        h, w, _ = pixels.shape
        length = "{0:08b}".format(len(data))
        data_bits = iter(
            length + "".join(["{0:08b}".format(ord(letter)) for letter in data])
        )

        encoded_image = pixels.copy()

        for y in range(py, h):
            for x in range(px, w):
                pixel = pixels[y, x]  # RGB Channels

                for i in range(3):
                    try:
                        bit = next(data_bits)
                        pixel[i] = pixel[i] & 0xFE | int(
                            bit
                        )  # Max value = FF, pixel[i] & FE isolates last bit, (...) | int(bit) encodes the bit (1 or 0)

                    except StopIteration:  # Message fully encoded!
                        break

                encoded_image[y, x] = pixel

        self.image = Image.fromarray(encoded_image)
        return

    def decode_LSB(self, px=0, py=0) -> str:
        pixels = np.asarray(self.image.convert("RGB"))

        h, w, _ = pixels.shape
        length = w * h - px * py  # default length
        data_bits = ""
        data = ""

        found_length = False  # Whether or not data length was counted already
        t = 0  # Number of characters extracted

        for y in range(py, h):
            for x in range(px, w):
                pixel = pixels[y, x]

                for i in range(3):
                    data_bits += str(pixel[i] & 1)

                while len(data_bits) >= 8:  # 8 bits per ASCII character
                    current_byte = data_bits[:8]
                    data_bits = data_bits[8:]

                    if not found_length:
                        length = int(current_byte, 2)
                        found_length = True
                        break

                    if t < length:  # Stop searching when the entire data is extracted
                        data += chr(int(current_byte, 2))
                        t += 1
                    else:
                        return data

    def encode_DCT(self, data):
        # Discrete Cosine Transform
        # May be a little tricky since we can't use processing libraries
        # IDK if this is even needed

        pass

    def decode_DCT(self):
        return


if __name__ == "__main__":
    img = Image.open(r"pixelheist\Engine\test\img\testimage.png")
    temp = ImageSteg(img)
    temp.encode_LSB("There is an impostor among us!", px=100, py=100)
    msg = temp.decode_LSB(px=100, py=100)
    print(msg)
