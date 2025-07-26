import os
import json
from pathlib import Path
import cv2
from PIL import Image
import subprocess

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
        
        # Create background with yellow border
        border_width = 3
        bg = Image.new('RGB', THUMBNAIL_SIZE, (255, 255, 0))  # Yellow background
        
        # Create inner area with black background
        inner_size = (THUMBNAIL_SIZE[0] - 2 * border_width, THUMBNAIL_SIZE[1] - 2 * border_width)
        inner_bg = Image.new('RGB', inner_size, (0, 0, 0))  # Black inner background
        
        # Paste inner background onto yellow border background
        bg.paste(inner_bg, (border_width, border_width))
        
        # Center the thumbnail image within the inner area
        x = border_width + (inner_size[0] - img.width) // 2
        y = border_width + (inner_size[1] - img.height) // 2
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

def convert_flv_to_mp4_opencv(flv_path, mp4_path=None):
    """Convert FLV file to MP4 using OpenCV (no FFmpeg dependency).
    
    Args:
        flv_path: Path to the input FLV file
        mp4_path: Path to the output MP4 file (optional, defaults to same name with .mp4 extension)
    
    Returns:
        str: Path to the converted MP4 file on success, None on failure
    """
    if not flv_path.lower().endswith('.flv'):
        return None
        
    if not os.path.exists(flv_path):
        return None
        
    if mp4_path is None:
        mp4_path = flv_path.rsplit('.', 1)[0] + '.mp4'
    
    try:
        # Use OpenCV to convert FLV to MP4
        input_cap = cv2.VideoCapture(flv_path)
        if not input_cap.isOpened():
            print(f"OpenCV cannot open FLV file: {flv_path}")
            return None
            
        # Get video properties
        fps = input_cap.get(cv2.CAP_PROP_FPS)
        width = int(input_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(input_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if fps <= 0:
            fps = 25.0  # Default fallback FPS
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(mp4_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print(f"Cannot create output MP4 file: {mp4_path}")
            input_cap.release()
            return None
        
        # Convert frame by frame
        frame_count = 0
        while True:
            ret, frame = input_cap.read()
            if not ret:
                break
            out.write(frame)
            frame_count += 1
        
        input_cap.release()
        out.release()
        
        if frame_count > 0 and os.path.exists(mp4_path):
            return mp4_path
        else:
            print(f"OpenCV conversion failed or no frames processed")
            return None
            
    except Exception as e:
        print(f"Error converting FLV to MP4 with OpenCV: {e}")
        return None

def convert_flv_to_mp4(flv_path, mp4_path=None, use_opencv=True):
    """Convert FLV file to MP4 using OpenCV (preferred) or FFmpeg fallback.
    
    Args:
        flv_path: Path to the input FLV file
        mp4_path: Path to the output MP4 file (optional, defaults to same name with .mp4 extension)
        use_opencv: Use OpenCV for conversion (True) or FFmpeg (False)
    
    Returns:
        str: Path to the converted MP4 file on success, None on failure
    """
    if use_opencv:
        # Try OpenCV first (no FFmpeg dependency)
        result = convert_flv_to_mp4_opencv(flv_path, mp4_path)
        if result:
            return result
        print("OpenCV conversion failed, falling back to FFmpeg...")
    
    # Fallback to FFmpeg if OpenCV fails or use_opencv=False
    if not flv_path.lower().endswith('.flv'):
        return None
        
    if not os.path.exists(flv_path):
        return None
        
    if mp4_path is None:
        mp4_path = flv_path.rsplit('.', 1)[0] + '.mp4'
    
    try:
        # Use FFmpeg to convert FLV to MP4
        cmd = [
            'ffmpeg', '-y',  # -y to overwrite output file
            '-i', flv_path,  # input file
            '-c:v', 'libx264',  # video codec
            '-c:a', 'aac',  # audio codec
            '-preset', 'fast',  # encoding preset for speed
            mp4_path  # output file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(mp4_path):
            return mp4_path
        else:
            print(f"FFmpeg conversion failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error converting FLV to MP4: {e}")
        return None
