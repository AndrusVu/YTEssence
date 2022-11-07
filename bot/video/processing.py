import os

import ffmpeg


def extract_video_frames(video_path: str, output_path: str):
    """Extract frames(every second) from Video file and save it in "output_path" folder"""

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_paths = os.path.join(output_path, "%06d.jpg")
    ffmpeg.input(video_path).filter("fps", fps="1").output(file_paths, start_number=0).run()
