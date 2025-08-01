# vchop

A standalone Python application for browsing directories, detecting video files, and performing advanced scene analysis and splitting with a sophisticated GUI interface.

## Features

### Core Functionality
- **Windowed GUI**: PyQt5-based user-friendly interface for desktop environments
- **Directory Browser**: Open and browse folders with automatic video file detection
- **Video Detection**: Automatically find and display video files (.mp4, .avi, .mov, .flv) as thumbnails
- **Scene Analysis**: Advanced scene detection using the `scenedetect` library with ContentDetector
- **Scene Splitting**: Split detected scenes into individual MP4 files with FFmpeg integration
- **Command-line Directory Launch**: Start with a directory parameter to immediately display videos

### Advanced Features
- **Recent Directories**: Persistent recent directory tracking with quick access menu
- **Scene Management**: Dedicated scene manager window for post-split scene organization
- **Drag-and-Drop Reordering**: Intuitive scene reordering through drag-and-drop interface
- **Keyboard Shortcuts**: 
  - `j` - Enter join/scene mode
  - `[` / `]` - Reorder scenes up/down
  - `Delete` - Remove selected scenes
- **Scene Persistence**: Automatic saving of scene order and preferences
- **Thumbnail Generation**: Automatic thumbnail creation for all videos using OpenCV
- **Multi-Selection**: Select multiple videos or scenes for batch operations
- **Scene Chaining**: Combine selected scenes into a single output video
- **FLV to MP4 Conversion**: Convert FLV files to MP4 format for better compatibility
- **Export Control**: User-selectable output directories for split scenes

### Data Management
- **Settings Persistence**: User preferences stored in `~/.vchop/`
- **Thumbnail Caching**: Efficient thumbnail storage in `.vchop/thumbnails/` subdirectories
- **Scene Order Files**: Automatic `scene_order.txt` files maintain custom scene arrangements

## Installation

### Option 1: Standalone Executable (Recommended for End Users)

Download the pre-built executable from the releases page or build it yourself:

1. **Download**: Get the latest release from GitHub releases
2. **Windows Installer**: Run `vchop-x.x.x-setup.exe` for easy installation
3. **Portable**: Extract and run the executable directly

### Option 2: Run from Source (For Developers)

1. Clone the repository:
```bash
git clone https://github.com/alienbrainfarm/vchop.git
cd vchop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed on your system for video processing.

### Option 3: Build Your Own Executable

See [BUILD.md](BUILD.md) for detailed instructions on creating standalone executables and Windows installers.

## Usage

### Basic Usage
```bash
# Launch with directory browser
python src/main.py

# Launch with specific directory
python src/main.py /path/to/video/directory
```

### Workflow
1. **Browse Videos**: Select a directory to view video thumbnails
2. **Analyze Scenes**: Double-click a video or use "Split by Scenes" to analyze
3. **Convert FLV Files**: Select FLV files and use "Convert FLV to MP4" for better compatibility
4. **Split Scenes**: Choose output directory and split video into individual scenes
5. **Manage Scenes**: Use the scene manager to reorder, delete, or export scenes
6. **Export**: Create final videos from your arranged scenes

## Requirements
- Python 3.7+
- PyQt5
- OpenCV (opencv-python)
- Pillow
- scenedetect
- FFmpeg (system dependency)

## License
See `LICENSE` for details.

## Documentation
See the `docs/` directory for the Product Requirements Document (PRD) and additional documentation.
