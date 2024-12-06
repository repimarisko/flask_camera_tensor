from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import eventlet

# Jika menggunakan TensorFlow atau PyTorch, uncomment import berikut
# import tensorflow as tf
# import torch

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def process_frame(frame_data):
    try:
        # Decode base64 string to bytes
        header, encoded = frame_data.split(',', 1)
        img_bytes = base64.b64decode(encoded)

        # Convert bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)

        # Decode image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is not None:
            # Konversi frame dari BGR ke RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Konversi frame ke tensor menggunakan NumPy
            tensor = np.array(rgb_frame)

            # Jika menggunakan TensorFlow
            # tensor = tf.convert_to_tensor(rgb_frame, dtype=tf.float32)
            
            # Jika menggunakan PyTorch
            # tensor = torch.from_numpy(rgb_frame).float()

            # Cetak bentuk tensor (opsional, untuk debug)
            print(f'Tensor shape: {tensor.shape}')

            # Anda dapat menambahkan pemrosesan lanjutan di sini
            
        else:
            print("Frame is None")
    
    except Exception as e:
        print(f"Error processing frame: {e}")

@socketio.on('video_frame')
def handle_video_frame(data):
    # Data adalah string base64 dari frame
    process_frame(data)
    
    # Kirim balasan ke klien setelah frame diproses
    emit('response', {'data': 'Frame received and processed'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='192.168.137.1', port=5000, debug=True)
