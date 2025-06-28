import logging
from os.path import exists
import yt_dlp
from pathlib import Path
from urllib.parse import quote_plus



def download_video(url: str)->str:
    """
    Скачивает видео по переданной ссылке,
    сохраняет в папку проекта /tmp/ссылка_на_видео.mp4
    """
    project_path = Path(__file__).resolve().parent
    tmp_dir = project_path / 'tmp'
    url_safe = quote_plus(url)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    file_name = str(tmp_dir / f'{url_safe}.mp4')
    error_of_download = "Big size"
    ydl_opts = {
        'max_filesize': 25 * 1024 * 1024,
        'outtmpl': file_name,
        'format': 'best[height<=1080][ext=mp4]',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'downloader': 'aria2c',
        'external_downloader_args': ['-x', '16', '-k', '1M']
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    if exists(file_name):
        return file_name
    return error_of_download

def delete_file(path: Path)->None:
    """
    Удаляет файл по указанному пути
    """
    try:
        path.unlink(missing_ok=True)
    except Exception as e:
        logging.error(e)
