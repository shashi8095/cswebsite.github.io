from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

cameras = [
    {"id": 1, "name": "Camera 1"},
    {"id": 2, "name": "Camera 2"},
    # Add more cameras here
]

@app.route('/')
def index():
    return render_template('index.html', cameras=cameras)

@app.route('/camera/<int:camera_id>')
def view_camera(camera_id):
    camera = next((c for c in cameras if c["id"] == camera_id), None)
    camera_name = camera["name"] if camera else "Unknown Camera"
    return render_template('camera_view.html', camera_id=camera_id, camera_name=camera_name)

@app.route('/captured_videos/<int:camera_id>')
def captured_videos(camera_id):
    camera = next((c for c in cameras if c["id"] == camera_id), None)
    camera_name = camera["name"] if camera else "Unknown Camera"
    video_files = os.listdir('videos')
    videos = [file for file in video_files if f'camera_{camera_id}_' in file]
    return render_template('captured_videos.html', camera_id=camera_id, camera_name=camera_name, videos=videos)

@app.route('/upload_video/<int:camera_id>', methods=['POST'])
def upload_video(camera_id):
    if 'video' in request.files:
        video = request.files['video']
        if video.filename != '':
            video.save(os.path.join('videos', f'camera_{camera_id}_{video.filename}'))
            return redirect(url_for('view_camera', camera_id=camera_id))
    return "Upload failed."

if __name__ == '__main__':
    app.run(debug=True)
