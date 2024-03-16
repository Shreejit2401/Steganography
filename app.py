from flask import Flask, render_template, request, send_file, url_for, jsonify, send_from_directory
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import json
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text')
def text():
    return render_template('text.html')

@app.route('/audio')
def audio():
    return render_template('audio.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Audio Integration
@app.route('/audio_hide', methods=['POST'])
def audio_hide():
    cover_audio = request.files['cover_audio']
    secret_audio = request.files['secret_audio']

    cover_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_audio.filename)
    secret_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], secret_audio.filename)
    cover_audio.save(cover_audio_path)
    secret_audio.save(secret_audio_path)

    output_stego_audio = "static/encoded.wav"
    output_decoded_audio = "static/decoded.wav"
    encode_lsb(cover_audio_path, secret_audio_path, output_stego_audio)
    decode_lsb(output_stego_audio, output_decoded_audio)

    cover_audio_url = url_for('static', filename=cover_audio.filename)
    secret_audio_url = url_for('static', filename=secret_audio.filename)
    stego_audio_url = url_for('static', filename=output_stego_audio)
    decoded_audio_url = url_for('static', filename=output_decoded_audio)

    return jsonify({
        'cover_audio_url': cover_audio_url,
        'secret_audio_url': secret_audio_url,
        'stego_audio_url': stego_audio_url,
        'decoded_audio_url': decoded_audio_url
    })

def encode_lsb(cover_audio, secret_audio, output_file):
    cover_rate, cover_data = wavfile.read(cover_audio)
    _, secret_data = wavfile.read(secret_audio)
    if len(cover_data) < len(secret_data):
        secret_data = secret_data[:len(cover_data)]
    elif len(cover_data) > len(secret_data):
        secret_data = np.pad(secret_data, (0, len(cover_data) - len(secret_data)), mode='constant')
    cover_data = np.array(cover_data, dtype=np.int16)
    secret_data = np.array(secret_data, dtype=np.int16)
    stego_data = cover_data.copy()
    for i in range(len(secret_data)):
        stego_data[i] = (cover_data[i] & 0xFFFC) | ((secret_data[i] & 0xC000) >> 14)
    wavfile.write(output_file, cover_rate, stego_data)

def decode_lsb(stego_audio, output_file, cutoff_freq=4000, order=5):
    stego_rate, stego_data = wavfile.read(stego_audio)
    secret_data = np.zeros_like(stego_data, dtype=np.int16)
    for i in range(len(stego_data)):
        secret_data[i] = (stego_data[i] & 0x0003) << 14

    b, a = butter(order, cutoff_freq, btype='low', fs=stego_rate, output='ba')
    filtered_secret_data = lfilter(b, a, secret_data)

    wavfile.write(output_file, stego_rate, np.int16(filtered_secret_data))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Text Integration
with open('merged_dictionary.json', 'r') as file:
    d = json.load(file)

@app.route('/text_hide', methods=['POST'])
def text_hide():
    input_data = request.get_json()
    secret_text = input_data['secretText']
    encoded_text = text_encode(secret_text)
    decoded_text = text_decode(encoded_text)
    return jsonify({'encodedText': encoded_text, 'decodedText': decoded_text})

def text_encode(input_str):
    words = input_str.split()
    word_dict = d

    replaced_words = [word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  

def text_decode(input_str):
    reverse_word_dict = {v: k for k, v in d.items()}
    words = input_str.split()  
    replaced_words = [reverse_word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Image Integration

def custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true - y_pred))

model_path = 'testedmodel.h5'
loaded_model = tf.keras.models.load_model(model_path, custom_objects={'custom_loss': custom_loss})

@app.route('/image_hide', methods=['POST'])
def image_hide():
    cover_image = request.files['cover_image']
    secret_image = request.files['secret_image']

    cover_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cover.jpg')
    secret_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'secret.jpg')

    cover_image.save(cover_image_path)
    secret_image.save(secret_image_path)

    def preprocess_image(image_path):
        img = Image.open(image_path)
        img = img.resize((64, 64))
        img_array = np.array(img) / 255.0
        return img_array

    secret_image_arr = preprocess_image(secret_image_path)
    cover_image_arr = preprocess_image(cover_image_path)

    secret_image_arr = np.expand_dims(secret_image_arr, axis=0)
    cover_image_arr = np.expand_dims(cover_image_arr, axis=0)

    encoded_image = loaded_model.layers[2]([cover_image_arr, secret_image_arr])
    decoded_image = loaded_model.layers[3](encoded_image)

    # encoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded.jpg')
    # decoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'decoded.jpg')

    encoded_image_pil = Image.fromarray((encoded_image.numpy()[0] * 255).astype(np.uint8))
    decoded_image_pil = Image.fromarray((decoded_image.numpy()[0] * 255).astype(np.uint8))

    encoded_image_pil.save('static/encoded_image.jpg')
    decoded_image_pil.save('static/decoded_image.jpg')

    return jsonify({
        'cover_image_url': url_for('static', filename=os.path.join('uploads', 'cover.jpg')),
        'secret_image_url': url_for('static', filename=os.path.join('uploads', 'secret.jpg')),
        'encoded_image_url': url_for('static', filename=os.path.join('uploads', 'encoded.jpg')),
        'decoded_image_url': url_for('static', filename=os.path.join('uploads', 'decoded.jpg'))
    })


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
