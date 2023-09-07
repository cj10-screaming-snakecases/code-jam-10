import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image

# Load the image with added noise
image_path = 'cj10-screaming-snakecases/Engine/test/img/flag_with_noise.png'
noisy_image = np.array(Image.open(image_path))

# Normalize pixel values to [0, 1]
noisy_image = noisy_image / 255.0


# Define the denoising autoencoder model
def create_denoising_autoencoder():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(None, None, 3)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2), padding='same'),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2), padding='same'),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.UpSampling2D((2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.UpSampling2D((2, 2)),
        tf.keras.layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


# Load the denoising autoencoder model
autoencoder = create_denoising_autoencoder()
autoencoder.load_weights('your_autoencoder_weights.h5')  # Replace with your model weights file

# Perform denoising
denoised_image = autoencoder.predict(np.expand_dims(noisy_image, axis=0))[0]

# Visualize the denoised image
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Noisy Image')
plt.imshow(noisy_image)
plt.axis('off')
plt.subplot(1, 2, 2)
plt.title('Denoised Image')
plt.imshow(denoised_image)
plt.axis('off')
plt.show()

# Extract the hidden flag (assuming you know its location)
flag_region = denoised_image[250:250 + 13, 250:250 + 100]  # Adjust the region as needed
flag = flag_region.copy() * 255.0  # Rescale to [0, 255]
flag = flag.astype(np.uint8)
flag_image = Image.fromarray(flag)
flag_image.save('decoded_flag.png')
