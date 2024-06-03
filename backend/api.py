import os
from flask import Flask, request, jsonify
import sys
from scripts.gradio.t2v_test import Text2Video
sys.path.insert(1, os.path.join(sys.path[0], 'lvdm'))
def run_text2video_examples(description):
    result_dir='./tmp/'
    text2video = Text2Video(result_dir=result_dir, save_fps=8, video_length=1, max_split_size_mb=1024)
    
    steps, cfg_scale, eta, fps = [25,12,1,16]
    print(f"Running example: {description}")
    video_path = text2video.get_prompt(description, steps, cfg_scale, eta, fps)
    print(f"Video saved to: {video_path}")

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    payload = request.get_json(force=True)
    print(payload)
    generate(payload['description'])

    # votame video results folderist kui generate valmis, siis returnime selle video
    return jsonify(payload['description'])

def generate(description):
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"  # Adjust max_split_size_mb as needed
    result_dir = os.path.join('./', 'results')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    run_text2video_examples(description)
    print('All examples processed.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

