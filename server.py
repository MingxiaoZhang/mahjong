import socketio
import eventlet
import eventlet.wsgi
import numpy as np
from PIL import Image
import io

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
def upload_image(sid, data):
    print("Received image from", sid)
    try:
        # Convert binary data to a NumPy array
        image = Image.open(io.BytesIO(data))
        image_array = np.asarray(image)
        print("Image converted to NumPy array with shape:", image_array.shape)
        # Further processing can be done here
        sio.emit("upload_ack", {"status": "success"}, room=sid)
    except Exception as e:
        print("Error processing image:", e)
        sio.emit("upload_ack", {"status": "failure", "error": str(e)}, room=sid)

@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
