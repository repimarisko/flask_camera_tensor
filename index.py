from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inisialisasi akses ke kamera (0 untuk kamera default)
camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        # Membaca frame dari kamera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Meng-encode frame menjadi format JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Mengirimkan frame dalam format byte untuk ditampilkan di browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Halaman utama untuk menampilkan video
    return render_template('index.html')

@app.route('/index')
def video_feed():
    # Endpoint untuk menampilkan video streaming
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
