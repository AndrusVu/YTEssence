import os
from pathlib import Path, PosixPath

import ffmpeg
from lavis.models import load_model_and_preprocess
from PIL import Image
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # setup device to use
MODEL, vis_processors, text_processors = load_model_and_preprocess(
    "blip_caption", "large_coco", device=DEVICE, is_eval=True
)


def _append_text(self: PosixPath, data: str, encoding=None, errors=None) -> None:
    """Open the file in text mode, write to it in append mode, and close the file."""
    if not isinstance(data, str):
        raise TypeError(f"data must be str, not {data.__class__.__name__}")
    with self.open(mode="a", encoding=encoding, errors=errors) as f:
        return f.write(data)


Path.append_text = _append_text


def extract_video_frames(video_path: str, output_path: str):
    """Extract frames(every second) from Video file and save it in "output_path" folder"""

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_paths = os.path.join(output_path, "%06d.jpg")
    ffmpeg.input(video_path).filter("fps", fps="1").output(file_paths, start_number=0).run()


def process_image(file_path: str) -> list[str]:
    """Convert images to Small text description"""
    # preprocessing
    raw_image = Image.open(file_path).convert("RGB")
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(DEVICE)  # preprocess image and text inputs

    # common_capture = MODEL.generate({"image": image})  # generate caption using beam search  # FIXME remove it

    # due to the non-determinstic nature of necleus sampling, you may get different captions.
    return MODEL.generate({"image": image}, use_nucleus_sampling=True, num_captions=3)


def frames_to_captions(frames_path: str, output_file_path: str):
    """Process all frames from folder and save it in output file."""
    file_names = (f for f in os.listdir(frames_path) if os.path.isfile(os.path.join(frames_path, f)))

    for start, file_name in enumerate(file_names):
        end = start + 1
        multiple_captions = process_image(os.path.join(frames_path, file_name))
        time_code = (
            f"{start // 3600:02}:{start // 3600 // 60:02}:{start % 60:02},000 "
            "-> "
            f"{end // 3600:02}:{end // 3600 // 60:02}:{end % 60:02},000"
        )  # aka 00:00:00,000 -> 00:00:01,000
        frame_info = f"{int(Path(file_name).stem)}\n{time_code}\n{'. '.join(multiple_captions)}\n\n"
        Path(output_file_path).append_text(frame_info)


def get_captions(file_path: str) -> str:
    """Get text from a file. After that reduce the size of the text to 1000 symbols."""
    return f"{Path(file_path).read_text()[:1000]}\n..."
