const video = document.getElementById('video');
const socket = io();

// Meminta akses ke kamera
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        
        // Mengambil frame dari video setiap 100 ms
        setInterval(() => {
            captureAndSendFrame();
        }, 100); // Anda dapat menyesuaikan interval sesuai kebutuhan
    })
    .catch(err => {
        console.error("Error accessing camera: " + err);
    });

function captureAndSendFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('video_frame', dataURL);
}
