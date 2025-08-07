"""
Constants used throughout the vchop application.

This module centralizes all magic numbers and configuration values
to improve maintainability and reduce duplication.
"""

# Video file extensions supported by the application
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.flv']

# Thumbnail configuration
THUMBNAIL_SIZE = (200, 200)
THUMBNAIL_DIR = '.vchop/thumbnails'
THUMBNAIL_BORDER_WIDTH = 3

# Color constants (RGB tuples)
COLORS = {
    'YELLOW': (255, 255, 0),    # Default thumbnail border
    'BLUE': (0, 0, 255),        # Scene mode thumbnail border
    'BLACK': (0, 0, 0),         # Inner background
}

# Directory and file management
MAX_RECENT_DIRS = 5
SETTINGS_DIR = '.vchop'
RECENT_DIRS_FILENAME = 'recent_dirs.json'
SCENE_ORDER_FILENAME = 'scene_order.txt'

# UI Configuration
DEFAULT_WINDOW_SIZE = (800, 600)
SCENE_MANAGER_WINDOW_SIZE = (900, 600)
LIST_WIDGET_SPACING = 10

# FFmpeg conversion settings
FFMPEG_PRESET = 'fast'
DEFAULT_FPS = 25.0