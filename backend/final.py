import os
import sys
from scripts.gradio.t2v_test import Text2Video
sys.path.insert(1, os.path.join(sys.path[0], 'lvdm'))

def generate_videos(prompts, steps, cfg_scale, eta, fps, result_dir='./tmp/'):
    text2video = Text2Video(result_dir)
    videos = []
    for prompt in prompts:
        video = text2video.get_prompt(prompt, steps, cfg_scale, eta, fps)
        videos.append(video)
    return videos

if __name__ == "__main__":
    result_dir = os.path.join('./', 'tulemused')
    
    # Define your parameters here
    prompts = ['random men kising blue red green']
    steps = 50
    cfg_scale = 12
    eta = 1.0
    fps = 16
    
    generated_videos = generate_videos(prompts, steps, cfg_scale, eta, fps, result_dir)
    
    for idx, video in enumerate(generated_videos):
        print(f"Generated video {idx+1} saved at: {video}")
