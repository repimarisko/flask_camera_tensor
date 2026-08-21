import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, Response, request
import cv2
import numpy as np

app = Flask(__name__)

def generate_frames():
    # Inisialisasi kamera dengan URL
    camera_url = "http://192.168.137.1:8080/video"
    camera = cv2.VideoCapture(camera_url)
    try:
        while True:
            # Baca frame dari kamera
            success, frame = camera.read()
            if not success:
                break
            else:
                # Ubah frame dari BGR ke RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Konversi frame ke tensor menggunakan NumPy
                tensor = np.array(rgb_frame)

                # Cetak bentuk tensor (opsional, untuk debug)
                print(f'Tensor shape: {tensor.shape}')

                # Encode frame ke format JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Yield frame dalam format multipart untuk streaming
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()

@app.route('/')
def index():
    # Render halaman utama
    return render_template('index.html')

@app.route('/index')
def video_feed():
    # Kembalikan generator frame
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
