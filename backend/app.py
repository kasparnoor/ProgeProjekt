import os
import sys
from scripts.gradio.t2v_test import Text2Video
sys.path.insert(1, os.path.join(sys.path[0], 'lvdm'))

def run_text2video_examples(result_dir='./tmp/'):
    text2video = Text2Video(result_dir=result_dir, save_fps=8, video_length=10, max_split_size_mb=1024)
    
    for example in t2v_examples:
        prompt, steps, cfg_scale, eta, fps = example
        print(f"Running example: {prompt}")
        video_path = text2video.get_prompt(prompt, steps, cfg_scale, eta, fps)
        print(f"Video saved to: {video_path}")

if __name__ == "__main__":
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"  # Adjust max_split_size_mb as needed
    result_dir = os.path.join('./', 'results')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    run_text2video_examples(result_dir)
    print('All examples processed.')
