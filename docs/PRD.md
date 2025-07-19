# Product Requirements Document (PRD)

## Project Overview
vchop is a standalone, windowed executable application built with Python and PyQt5. The application provides comprehensive video management capabilities including directory browsing, automatic video file detection, advanced scene analysis, and sophisticated scene splitting and management features.

## Implemented Features

### Core Video Management
- **Windowed GUI**: PyQt5-based desktop application with modern interface
- **Directory Browser**: Open and browse folders with persistent recent directory tracking
- **Video Detection**: Automatically detect and display video files (.mp4, .avi, .mov) with thumbnail previews
- **Multi-Selection**: Support for selecting multiple videos or scenes for batch operations
- **Command-line Directory Launch**: Launch with directory parameter for immediate video display

### Advanced Scene Processing
- **Scene Analysis**: Advanced scene detection using `scenedetect` library with ContentDetector algorithm
- **Scene Splitting**: Split videos into individual MP4 files using FFmpeg with lossless copy codec
- **Scene Manager**: Dedicated window for managing split scenes with visual thumbnails
- **Scene Chaining**: Combine selected scenes into single output videos
- **Custom Output Selection**: User-controlled output directory selection for all operations

### User Experience Enhancements
- **Drag-and-Drop Scene Reordering**: Intuitive scene arrangement through drag-and-drop
- **Keyboard Shortcuts**: 
  - `j` - Toggle between video browser and scene management mode
  - `[` - Move selected scene up in order
  - `]` - Move selected scene down in order  
  - `Delete` - Remove selected scenes from project
- **Thumbnail Generation**: Automatic thumbnail creation and caching for all video content
- **Scene Persistence**: Automatic saving and loading of scene arrangements via `scene_order.txt` files

### Data Management
- **Settings Persistence**: User preferences and recent directories stored in `~/.vchop/` directory
- **Thumbnail Caching**: Efficient thumbnail storage in `.vchop/thumbnails/` subdirectories
- **Scene Order Management**: Persistent scene arrangement with automatic file-based storage
- **Error Handling**: Comprehensive error handling for video processing and file operations

## Functional Requirements (Implemented)

### Primary Functions
1. **Directory Navigation**: Browse and select directories with recent directory persistence
2. **Video Display**: Display video files as thumbnail icons with metadata
3. **Video Processing**: Launch video editor for scene analysis and splitting
4. **Scene Detection**: Automatic scene boundary detection using content-based algorithms
5. **Scene Export**: Export individual scenes as separate MP4 files with user-selected output location
6. **Scene Management**: Post-processing scene arrangement, reordering, and deletion
7. **Scene Joining**: Combine multiple scenes into single output videos
8. **Command-line Integration**: Direct directory launching via command-line arguments

### Advanced Functions
9. **Drag-and-Drop Reordering**: Visual scene arrangement through intuitive drag-and-drop
10. **Keyboard Navigation**: Comprehensive keyboard shortcuts for power users
11. **Thumbnail Management**: Automatic thumbnail generation and caching system
12. **Multi-Window Interface**: Separate windows for video browsing and scene management
13. **Batch Operations**: Multi-selection support for batch scene processing

## Technical Implementation

### Architecture
- **Main Application**: `main.py` - Application entry point with command-line parameter support
- **Video Browser**: `video_browser.py` - Primary interface for video discovery and management
- **Video Editor**: `video_editor.py` - Scene analysis and splitting functionality
- **Scene Manager**: `scene_manager_window.py` - Advanced scene arrangement and export
- **Utilities**: `video_utils.py` - Core video processing and file management utilities

### Technology Stack
- **Python 3.7+** (core language)
- **PyQt5** (GUI framework with advanced widgets)
- **OpenCV** (video processing and thumbnail generation)
- **Pillow** (image processing and thumbnail optimization)
- **scenedetect** (advanced scene detection algorithms)
- **FFmpeg** (video encoding and processing backend)

### Dependencies
```
PyQt5>=5.15.0
opencv-python>=4.5.0
Pillow>=8.0.0
scenedetect>=0.6.0
tqdm>=4.60.0
```

## Non-Functional Requirements

### Performance
- **Fast Video Scanning**: Efficient directory traversal with thumbnail caching
- **Accurate Scene Detection**: Content-based scene boundary detection with configurable sensitivity
- **Responsive UI**: Non-blocking operations with progress feedback
- **Memory Management**: Efficient thumbnail caching with automatic cleanup

### Compatibility
- **Cross-platform**: Windows, macOS, Linux support through PyQt5
- **Video Format Support**: MP4, AVI, MOV with extensible format detection
- **File System Integration**: Native directory dialogs and file operations

### Usability
- **Intuitive Interface**: Icon-based video browsing with visual feedback
- **Error Handling**: Comprehensive error messages and graceful failure recovery
- **Accessibility**: Keyboard navigation and screen reader compatibility
- **Documentation**: Comprehensive README and inline help

## Project Status

### Completed Milestones ✅
1. ✅ Project structure and PyQt5 GUI framework
2. ✅ Directory browsing with recent directory persistence  
3. ✅ Video thumbnail display with caching system
4. ✅ Video selection and advanced scene analysis
5. ✅ Scene splitting with FFmpeg integration
6. ✅ Scene management with drag-and-drop reordering
7. ✅ Keyboard shortcuts and power user features
8. ✅ Data persistence and settings management

### Future Enhancements
- [ ] Executable packaging with PyInstaller
- [ ] Additional video format support (MKV, WMV, etc.)
- [ ] Scene detection parameter tuning interface
- [ ] Batch video processing capabilities
- [ ] Video preview playback integration
- [ ] Export format options (different codecs, quality settings)

---
*Last updated: January 2025*
