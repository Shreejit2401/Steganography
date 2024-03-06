import numpy as np
from scipy.io import wavfile
# from IPython.display import Audio
from scipy.signal import butter, lfilter

def encode_lsb(cover_audio, secret_audio, output_file):
    cover_rate, cover_data = wavfile.read(cover_audio)
    secret_rate, secret_data = wavfile.read(secret_audio)
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

cover_audio = "D:/Steganography/sample audios/audio2.wav"
secret_audio = "D:/Steganography/sample audios/audio3.wav"
output_stego_audio = "D:/Steganography/output audios/encoded.wav"
output_decoded_audio = "D:/Steganography/output audios/decoded.wav"

encode_lsb(cover_audio, secret_audio, output_stego_audio)
decode_lsb(output_stego_audio, output_decoded_audio)
