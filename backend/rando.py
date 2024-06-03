import os
import sys
import glob
from flask import Flask, request, jsonify, send_file, render_template
from scripts.gradio.t2v_test import Text2Video
sys.path.insert(1, os.path.join(sys.path[0], 'lvdm'))

def generate_videos(prompt, steps, cfg_scale, eta, fps, result_dir='./tmp/', result_file_name=None):
    text2video = Text2Video(result_dir,gpu_num=1, save_fps=8, video_length=1, max_split_size_mb=1024, result_file_name=result_file_name)
    videos = []
    video = text2video.get_prompt(prompt, steps, cfg_scale, eta, fps)
    videos.append(video)
    return videos

result_dir = os.path.join('./', 'tulemused')


app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    payload = request.get_json(force=True)
    print(payload)
    description = payload['description']
    result_file_name = payload['filename']
    steps = 50
    cfg_scale = 12
    eta = 1.0
    fps = 1
    
    generated_videos = generate_videos(description, steps, cfg_scale, eta, fps, result_dir, result_file_name)
    
    for idx, video in enumerate(generated_videos):
        print("File path:", f"{video}")
        # votame video results folderist kui generate valmis, siis returnime selle video
        if os.path.exists(f"{video}"):
            return send_file(f"{video}", as_attachment=True)
        else:
            return 'Video not found', 404

@app.route('/ping')
def ping():
    return jsonify(' Tere siuu siin kauri server')


@app.route('/files')
def files():
    BASE_DIR = 'tulemused/'
    all_files = glob.glob(f'{BASE_DIR}*.mp4')
    all_files = [f.replace(BASE_DIR,'') for f in all_files]
    print(all_files)
    return jsonify({'files' : all_files})



@app.route('/get_file/<filename>')
def get_file(filename=None):
    BASE_DIR = 'tulemused/'
    all_files = glob.glob(f'{BASE_DIR}*.mp4')
    all_files = [f.replace(BASE_DIR,'') for f in all_files]
    if filename in all_files:
        file_path = f'{BASE_DIR}{filename}'
        return send_file(file_path)
    else:
        return 'File not found', 404

@app.route('/')
def index():
    BASE_DIR = 'tulemused/'
    all_files = glob.glob(f'{BASE_DIR}*.mp4')
    all_files = [f.replace(BASE_DIR,'') for f in all_files]
    print(all_files)
    return render_template('files.html', all_files=all_files)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080)