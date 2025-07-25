import os
import json
from pathlib import Path
import cv2
from PIL import Image

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.flv']
THUMBNAIL_SIZE = (200, 200)
THUMBNAIL_DIR = '.vchop/thumbnails'
RECENT_DIRS_PATH = Path.home() / '.vchop' / 'recent_dirs.json'
MAX_RECENT = 5

def is_video_file(filename):
    return any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)

def create_thumbnail(filepath, thumb_path):
    cap = cv2.VideoCapture(filepath)
    success, frame = cap.read()
    cap.release()
    if success:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
        bg = Image.new('RGB', THUMBNAIL_SIZE, (0, 0, 0))
        x = (THUMBNAIL_SIZE[0] - img.width) // 2
        y = (THUMBNAIL_SIZE[1] - img.height) // 2
        bg.paste(img, (x, y))
        bg.save(thumb_path)
        return True
    return False

def load_recent_dirs():
    try:
        if RECENT_DIRS_PATH.exists():
            with open(RECENT_DIRS_PATH, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def update_recent_dirs(dir_path, recent_dirs):
    dirs = [dir_path] + [d for d in recent_dirs if d != dir_path]
    recent_dirs = dirs[:MAX_RECENT]
    RECENT_DIRS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RECENT_DIRS_PATH, 'w') as f:
        json.dump(recent_dirs, f)
    return recent_dirs
