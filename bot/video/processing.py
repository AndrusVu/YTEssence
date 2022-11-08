import os

import ffmpeg
from lavis.models import load_model_and_preprocess
from PIL import Image
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # setup device to use
MODEL, vis_processors, text_processors = load_model_and_preprocess(
    "blip_caption", "large_coco", device=DEVICE, is_eval=True
)


def extract_video_frames(video_path: str, output_path: str):
    """Extract frames(every second) from Video file and save it in "output_path" folder"""

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_paths = os.path.join(output_path, "%06d.jpg")
    ffmpeg.input(video_path).filter("fps", fps="1").output(file_paths, start_number=0).run()


def process_image(file_path: str) -> list[str]:
    # preprocessing
    raw_image = Image.open(file_path).convert("RGB")
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(DEVICE)  # preprocess image and text inputs

    # common_capture = MODEL.generate({"image": image})  # generate caption using beam search  # FIXME remove it

    # due to the non-determinstic nature of necleus sampling, you may get different captions.
    return MODEL.generate({"image": image}, use_nucleus_sampling=True, num_captions=3)
