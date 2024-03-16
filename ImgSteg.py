import tensorflow as tf
from PIL import Image
import numpy as np

def custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true - y_pred))

model_path = 'testedmodel.h5'
loaded_model = tf.keras.models.load_model(model_path, custom_objects={'custom_loss': custom_loss})

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((64, 64))
    img_array = np.array(img) / 255.0
    return img_array

secret_image_path = 'secret.jpg'
cover_image_path = 'cover.jpg'

secret_image = preprocess_image(secret_image_path)
cover_image = preprocess_image(cover_image_path)

secret_image = np.expand_dims(secret_image, axis=0)
cover_image = np.expand_dims(cover_image, axis=0)

encoded_image = loaded_model.layers[2]([cover_image, secret_image])

decoded_image = loaded_model.layers[3](encoded_image)

encoded_image = encoded_image.numpy()[0]
decoded_image = decoded_image.numpy()[0]

encoded_image_pil = Image.fromarray((encoded_image * 255).astype(np.uint8))
decoded_image_pil = Image.fromarray((decoded_image * 255).astype(np.uint8))

encoded_image_pil.save('encoded_image.jpg')
decoded_image_pil.save('decoded_image.jpg')