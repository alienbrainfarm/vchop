# Product Requirements Document (PRD)

## Project Overview
Create a standalone, windowed executable application using Python. The app will allow users to open directories, automatically detect video files, and display them as icons in the main window. Users can select videos and perform various functions, including scene analysis and splitting scenes into separate MP4 files.

## Features
- **Windowed GUI**: User-friendly interface for desktop environments.
- **Directory Browser**: Open and browse folders to locate video files.
- **Video Detection**: Automatically find and list video files (e.g., MP4, AVI, MOV) as icons.
- **Video Selection**: Select one or more videos for further actions.
- **Scene Analysis**: Analyze selected videos to detect scene boundaries.
- **Scene Splitting**: Split detected scenes into individual MP4 files and save them. When splitting, a dialog will open to select the output directory for the produced files.
- **Command-line Directory Launch**: Start the application with a directory parameter to immediately open and display thumbnails of all videos in that directory.

## Functional Requirements
1. **Open Directory**: User can select a folder; app scans for video files.
2. **Display Videos**: Show video files as clickable icons/thumbnails.
3. **Select Video**: User can select a video for processing.
4. **Analyze Scenes**: Detect scene changes in the selected video.
5. **Split Scenes**: Export each detected scene as a separate MP4 file. Prompt user with a dialog to select the output directory for the files.
6. **Start with Directory Parameter**: If a directory is provided as a command-line argument, open that directory and display video thumbnails on launch.

## Non-Functional Requirements
- Cross-platform compatibility (Windows, macOS, Linux).
- Fast and accurate video scanning and scene detection.
- Intuitive and responsive UI.
- Error handling for unsupported formats and failed operations.

## Technology Stack
- **Python** (core language)
- **GUI Framework**: PyQt, Tkinter, or similar
- **Video Processing**: OpenCV, MoviePy, or FFmpeg
- **Packaging**: PyInstaller or similar for executable builds

## Milestones
1. Set up project structure and GUI framework
2. Implement directory browsing and video detection
3. Display video icons/thumbnails
4. Add video selection and scene analysis
5. Implement scene splitting and export
6. Package as standalone executable

---
*Last updated: 13 July 2025*
