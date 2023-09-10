from PIL import Image


def reverse_color_shift(encrypted_image_path, constant_value, output_image_path):
    try:

        encrypted_image = Image.open(encrypted_image_path)
        decrypted_image = Image.new(encrypted_image.mode, encrypted_image.size)

        width, height = encrypted_image.size
        step = 0

        # Iterate through each pixel of the encrypted image
        for x in range(width):
            for y in range(height):
                r, g, b = encrypted_image.getpixel((x, y))

                # Reverse color shift
                r = (r - (constant_value + step)) % 256
                g = (g - (constant_value + step)) % 256
                b = (b - (constant_value + step)) % 256

                # Set the decrypted pixel in the output image
                decrypted_image.putpixel((x, y), (r, g, b))

                step += 1

        # Save the decrypted image
        decrypted_image.save(output_image_path)
        print(f'Decrypted image saved to {output_image_path}')

    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    encrypted_image_path = 'pixelheist/Engine/test/img/flag_color_shift.png'
    constant_value = 136  # Needs to be provided by the suer
    output_image_path = 'pixelheist/Engine/test/img/decrypted_flag_color_shift.png'

    reverse_color_shift(encrypted_image_path, constant_value, output_image_path)
