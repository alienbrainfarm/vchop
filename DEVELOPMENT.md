# Development Setup Guide

This guide helps developers set up their environment for contributing to vchop.

## Prerequisites

- Python 3.7 or higher
- Git
- FFmpeg (for video processing)

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/alienbrainfarm/vchop.git
cd vchop
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 isort pytest
```

### 4. Install FFmpeg

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS (with Homebrew):
```bash
brew install ffmpeg
```

#### Windows:
Download from https://ffmpeg.org/download.html and add to PATH.

## Development Workflow

### Code Style

We use Black for code formatting and flake8 for linting:

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Sort imports
isort src/ tests/
```

### Running Tests

```bash
# Run all tests
PYTHONPATH=src python -m unittest discover tests/ -v

# Run specific test
PYTHONPATH=src python -m unittest tests.test_video_utils -v
```

### Running the Application

```bash
# Run from source
PYTHONPATH=src python src/main.py

# Run with specific directory
PYTHONPATH=src python src/main.py /path/to/videos
```

## Project Structure

```
vchop/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── video_browser.py   # Main GUI window
│   ├── video_utils.py     # Core utilities
│   ├── scene_manager_window.py  # Scene management
│   └── logging_config.py  # Logging setup
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── requirements.txt       # Runtime dependencies
├── pyproject.toml        # Development tool configuration
└── README.md             # Project documentation
```

## Common Tasks

### Adding New Features

1. Create a new branch: `git checkout -b feature/your-feature`
2. Write tests for your feature
3. Implement the feature
4. Run tests and ensure they pass
5. Format code with Black
6. Create pull request

### Debugging

The application uses Python's logging module. Logs are written to:
- Console (stdout)
- `~/.vchop/logs/vchop.log` (if logging to file is enabled)

To enable debug logging, modify the logging level in `main.py`:
```python
setup_logging(level=logging.DEBUG)
```

### Building Executable

See [BUILD.md](BUILD.md) for detailed instructions on creating standalone executables.

## Contributing Guidelines

1. Follow PEP 8 style guidelines (enforced by flake8)
2. Write tests for new functionality
3. Update documentation for user-facing changes
4. Use descriptive commit messages
5. Keep pull requests focused and small

## Troubleshooting

### Common Issues

**PyQt5 import errors:**
- Ensure you're in the virtual environment
- Try: `pip install --upgrade PyQt5`

**FFmpeg not found:**
- Verify FFmpeg is installed and in PATH
- Test with: `ffmpeg -version`

**Test failures in headless environment:**
- GUI tests may fail without display
- Use `Xvfb` on Linux: `xvfb-run python -m unittest`

**Permission errors:**
- Ensure write permissions to `~/.vchop/` directory
- Check video file permissions

For more help, check the project's issue tracker or documentation in the `docs/` directory.