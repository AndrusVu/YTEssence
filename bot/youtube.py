import logging
import os
from typing import Any, Optional

from pytube import YouTube


_logger = logging.getLogger(__name__)


def on_complete(stream: Any, file_path: Optional[str]):
    _logger.info("Downloaded successfully.")


def download_video(url: str, destination_path: str):
    yt = YouTube(url, on_complete_callback=on_complete, use_oauth=False)

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        _logger.debug("Destination folder for downloaded file was created.")
    yt.streams.filter(file_extension="mp4", res="720p").first().download(destination_path)
