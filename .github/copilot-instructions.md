# GitHub Copilot Instructions

These instructions define how GitHub Copilot should assist with the vchop project. The goal is to ensure consistent, high-quality code generation aligned with our conventions, stack, and best practices.

## 🧠 Context

- **Project Type**: Desktop GUI Application for Video Processing and Scene Analysis
- **Language**: Python 3.7+
- **GUI Framework**: PyQt5
- **Video Processing Libraries**: OpenCV, scenedetect, Pillow, FFmpeg
- **Architecture**: Modular GUI application with separate concerns (browser, utils, scene management)
- **Build Target**: Standalone executable via PyInstaller

## 🔧 General Guidelines

- Follow PEP 8 style guidelines and use type hints where applicable
- Use Black for code formatting (line length: 88), isort for import ordering
- Emphasize readability and maintainability over clever one-liners
- Use meaningful variable and function names that describe video/GUI operations
- Handle video processing errors gracefully with user-friendly messages
- Ensure thread safety for GUI operations and video processing
- Use logging for debugging video operations and user actions

## 📁 File Structure

Use this structure when creating or updating files:

```text
src/
  main.py                 # Application entry point
  video_browser.py        # Main GUI window and video browsing
  video_utils.py          # Core video processing utilities  
  scene_manager_window.py # Scene management GUI
  logging_config.py       # Logging configuration
  __version__.py          # Version information
tests/
  test_*.py              # Unit tests for each module
docs/                    # Documentation files
build.py                 # Build script for executables
requirements.txt         # Python dependencies
pyproject.toml          # Code quality tool configuration
```

## 🎬 Video Processing Patterns

### ✅ Patterns to Follow

- **Error Handling**: Always validate video file paths and handle FFmpeg/OpenCV errors gracefully
- **Thumbnail Generation**: Use OpenCV for consistent thumbnail creation with proper aspect ratio handling
- **Scene Detection**: Leverage scenedetect library with ContentDetector for reliable scene boundary detection
- **File Format Support**: Support common video formats (.mp4, .avi, .mov, .flv) with appropriate conversions
- **Progress Feedback**: Use tqdm or QProgressBar for long-running video operations
- **Memory Management**: Release video resources properly to prevent memory leaks
- **Settings Persistence**: Store user preferences in `~/.vchop/` directory
- **Thread Safety**: Use QThread for video processing to keep GUI responsive

### 🚫 Patterns to Avoid

- Don't block the main GUI thread with video processing operations
- Avoid hardcoded video formats or resolutions
- Don't process videos without checking if files exist and are readable
- Avoid storing video data in memory longer than necessary
- Don't ignore FFmpeg exit codes or OpenCV exceptions
- Avoid platform-specific file paths (use os.path or pathlib)

## 🖼️ GUI Development Guidelines

### PyQt5 Best Practices

- Use proper parent-child widget relationships for memory management
- Connect signals and slots appropriately for user interactions
- Use QFileDialog for file/directory selection with appropriate filters
- Implement proper window sizing and responsive layouts
- Handle window close events gracefully
- Use QMessageBox for user notifications and confirmations
- Implement keyboard shortcuts for common operations (j, [, ], Delete)

### Drag and Drop

- Implement drag-and-drop for file/scene reordering where appropriate
- Use proper MIME types for file operations
- Provide visual feedback during drag operations

## 🧪 Testing Guidelines

- Use unittest for all test cases with descriptive test method names
- Mock video file operations and external dependencies (FFmpeg, scenedetect)
- Test both successful video processing and error conditions
- Use temporary files for tests that require actual video data
- Test GUI components with QTest framework where appropriate
- Ensure tests can run in headless environments (use Xvfb if needed)
- Test cross-platform compatibility (Windows, Linux, macOS)

## 🔧 Development Workflow

### Code Quality

- Run pre-commit hooks before committing (black, flake8, isort)
- Use PYTHONPATH=src when running modules during development
- Test on multiple video formats and edge cases
- Verify GUI responsiveness during video processing
- Check memory usage with large video files

### Building and Distribution

- Use PyInstaller for creating standalone executables
- Test executables on clean systems without Python installed
- Verify all video processing dependencies are bundled correctly
- Create Windows installers with NSIS when needed

## 🎯 Common Tasks Examples

### Video Processing
```python
# Generate thumbnail with error handling
def create_thumbnail(video_path: str, output_path: str, timestamp: float = 1.0) -> bool:
    """Create thumbnail from video at specified timestamp."""
    cap = cv2.VideoCapture(video_path)
    try:
        # Implementation with proper error handling
        pass
    finally:
        cap.release()
```

### GUI Components
```python
# PyQt5 widget with proper signal handling
class VideoListWidget(QListWidget):
    video_selected = pyqtSignal(str)  # Custom signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemDoubleClicked.connect(self.on_video_double_click)
```

### Scene Management
```python
# Scene detection with progress feedback
def detect_scenes(video_path: str, progress_callback=None) -> List[Scene]:
    """Detect scenes in video with optional progress updates."""
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    # Implementation with progress reporting
```

## 🧩 Example Prompts

- `Create a PyQt5 dialog for selecting video output directory with remember preference`
- `Implement scene reordering with drag-and-drop functionality in the scene manager`
- `Add FFmpeg error handling for video conversion with user-friendly error messages`
- `Write a unit test for thumbnail generation that mocks OpenCV operations`
- `Create a method to validate video file integrity before processing`

## 🔄 Code Review Guidelines

- Ensure video operations don't block the GUI thread
- Verify proper resource cleanup (file handles, video captures)
- Check error handling covers common video processing failures
- Validate GUI components follow PyQt5 conventions
- Ensure cross-platform compatibility for file operations
- Test with various video formats and edge cases

## 📚 References

- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [OpenCV Python Documentation](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [scenedetect Documentation](https://scenedetect.readthedocs.io/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [tqdm Progress Bars](https://tqdm.github.io/)

## 🎮 Application-Specific Context

vchop is a video file browser and scene detection tool that allows users to:
- Browse directories and view video files as thumbnails
- Analyze videos for scene boundaries using content detection
- Split videos into separate scene files
- Manage and reorder detected scenes
- Convert FLV files to MP4 format
- Export selected scenes as combined videos

The application emphasizes user experience with responsive GUI, persistent settings, and robust error handling for video operations.