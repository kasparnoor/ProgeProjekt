import os
import time
from omegaconf import OmegaConf
import torch
from torch.utils.data import DataLoader
from scripts.evaluation.funcs import load_model_checkpoint, save_videos, batch_ddim_sampling
from utils.utils import instantiate_from_config
from huggingface_hub import hf_hub_download
from torch.cuda.amp import autocast, GradScaler

class Text2Video():
    def __init__(self, result_dir='./tmp/', gpu_num=1, save_fps=8, video_length=1, max_split_size_mb=1024, result_file_name=None):
        self.download_model()
        self.result_dir = result_dir
        self.save_fps = save_fps
        self.video_length = video_length
        self.max_split_size_mb = max_split_size_mb
        self.result_file_name = result_file_name
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        
        ckpt_path = 'checkpoints/base_512_v2/model.ckpt'
        config_file = 'configs/inference_t2v_512_v2.0.yaml'
        config = OmegaConf.load(config_file)
        model_config = config.pop("model", OmegaConf.create())
        model_config['params']['unet_config']['params']['use_checkpoint'] = False   
        model_list = []
        
        for gpu_id in range(gpu_num):
            model = instantiate_from_config(model_config)
            assert os.path.exists(ckpt_path), "Error: checkpoint Not Found!"
            model = load_model_checkpoint(model, ckpt_path)
            model.eval()
            model_list.append(model)
        
        self.model_list = model_list
        self.scaler = GradScaler()  # For mixed precision training

    def get_prompt(self, prompt,  steps=50, cfg_scale=12.0, eta=1.0, fps=16, result_file_name=None):
        torch.cuda.empty_cache()
        print('start:', prompt, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        start = time.time()
        gpu_id = 0
        if steps > 60:
            steps = 60
        
        model = self.model_list[gpu_id]
        model = model.cuda()
        batch_size = 1  # Reduce batch size to manage memory usage
        channels = model.model.diffusion_model.in_channels
        frames = self.video_length * self.save_fps  # calculate the number of frames based on the desired video length and FPS
        h, w = 320 // 8, 512 // 8
        noise_shape = [batch_size, channels, frames, h, w]

        # text cond
        text_emb = model.get_learned_conditioning([prompt])
        cond = {"c_crossattn": [text_emb], "fps": fps}
        
        ## inference
        with autocast():  # Enable mixed precision training
            batch_samples = batch_ddim_sampling(
                model, cond, noise_shape, n_samples=1, ddim_steps=steps, ddim_eta=eta, cfg_scale=cfg_scale, max_split_size_mb=self.max_split_size_mb)
        
        ## b, samples, c, t, h, w
        prompt_str = prompt.replace("/", "_slash_") if "/" in prompt else prompt
        prompt_str = prompt_str.replace(" ", "_") if " " in prompt else prompt_str
        prompt_str = prompt_str[:30]

        if result_file_name:
            save_videos(batch_samples, self.result_dir, filenames=[result_file_name], fps=self.save_fps)
        else:
            save_videos(batch_samples, self.result_dir, filenames=[prompt_str], fps=self.save_fps)
        print(f"Saved in {prompt_str}. Time used: {(time.time() - start):.2f} seconds")
        model = model.cpu()
        return os.path.join(self.result_dir, f"{prompt_str}.mp4")
    
    def download_model(self):
        REPO_ID = 'VideoCrafter/VideoCrafter2'
        filename_list = ['model.ckpt']
        if not os.path.exists('./checkpoints/base_512_v2/'):
            os.makedirs('./checkpoints/base_512_v2/')
        for filename in filename_list:
            local_file = os.path.join('./checkpoints/base_512_v2/', filename)
            if not os.path.exists(local_file):
                hf_hub_download(repo_id=REPO_ID, filename=filename, local_dir='./checkpoints/base_512_v2/', local_dir_use_symlinks=False)

if __name__ == '__main__':
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"  # Adjust max_split_size_mb as needed
    t2v = Text2Video(save_fps=8, video_length=5, max_split_size_mb=1024)
    video_path = t2v.get_prompt('a black swan swims on the pond')
    print('done', video_path)
