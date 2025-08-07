# Troubleshooting Guide

This guide helps resolve common issues when using or developing vchop.

## Common Installation Issues

### FFmpeg Not Found

**Problem**: Error messages about FFmpeg not being found or video conversion failing.

**Solution**:
1. Install FFmpeg for your operating system:
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html
2. Verify installation: `ffmpeg -version`
3. Ensure FFmpeg is in your system PATH

### PyQt5 Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**:
1. Ensure you're using Python 3.7+: `python --version`
2. Install PyQt5: `pip install PyQt5`
3. On Linux, you may need: `sudo apt install python3-pyqt5`

### OpenCV Issues

**Problem**: Issues with video thumbnail generation or conversion.

**Solution**:
1. Reinstall OpenCV: `pip uninstall opencv-python && pip install opencv-python`
2. For headless servers: `pip install opencv-python-headless`
3. Check video file permissions and format compatibility

## Runtime Issues

### Application Won't Start

**Problem**: Application crashes on startup or won't display window.

**Solution**:
1. Check log files in `~/.vchop/logs/vchop.log`
2. Ensure you have a display (for GUI applications)
3. Try running with debug logging:
   ```bash
   PYTHONPATH=src python -c "
   from logging_config import setup_logging
   import logging
   setup_logging(level=logging.DEBUG)
   from main import main
   main()
   "
   ```

### Directory Permission Errors

**Problem**: Cannot access or save to directories.

**Solution**:
1. Check write permissions for `~/.vchop/` directory
2. Ensure video directories are readable
3. Run with appropriate user permissions

### Thumbnail Generation Fails

**Problem**: Videos display without thumbnails.

**Solution**:
1. Check video file format compatibility (.mp4, .avi, .mov, .flv)
2. Verify video files are not corrupted
3. Check disk space for thumbnail cache
4. Clear thumbnail cache: Delete `~/.vchop/thumbnails/`

## Scene Detection Issues

### No Scenes Detected

**Problem**: Scene analysis completes but no scenes are found.

**Solution**:
1. Verify video has actual scene changes
2. Try different scene detection sensitivity (if configurable)
3. Check video codec compatibility
4. Ensure video duration is sufficient

### Scene Splitting Fails

**Problem**: Scene analysis works but splitting fails.

**Solution**:
1. Ensure sufficient disk space for output files
2. Check output directory permissions
3. Verify FFmpeg installation and configuration
4. Try with different video files to isolate the issue

## Performance Issues

### Slow Thumbnail Generation

**Problem**: Application is slow when browsing directories with many videos.

**Solution**:
1. Thumbnails are cached - first access will be slower
2. Consider smaller video files for testing
3. Check available system resources (RAM, CPU)
4. Close other resource-intensive applications

### Large Memory Usage

**Problem**: Application uses too much memory.

**Solution**:
1. Restart the application periodically
2. Close scene manager windows when not needed
3. Clear thumbnail cache if it becomes too large
4. Consider processing fewer videos at once

## Development Issues

### Tests Fail in Headless Environment

**Problem**: GUI tests fail on CI/headless servers.

**Solution**:
1. Use virtual display: `xvfb-run python -m unittest`
2. Mock GUI components in tests
3. Skip GUI tests in headless environments
4. Use pytest with appropriate markers

### Code Style Issues

**Problem**: Code doesn't match project style guidelines.

**Solution**:
1. Install development tools: `pip install black flake8 isort`
2. Format code: `black src/ tests/`
3. Check style: `flake8 src/ tests/`
4. Sort imports: `isort src/ tests/`

### Import Errors in Tests

**Problem**: `ModuleNotFoundError` when running tests.

**Solution**:
1. Set Python path: `PYTHONPATH=src python -m unittest`
2. Use relative imports in test files
3. Ensure test directory structure matches source

## Getting Help

### Log Files

Check these log files for detailed error information:
- `~/.vchop/logs/vchop.log` - Application logs
- Console output when running from terminal

### Collecting Debug Information

When reporting issues, include:
1. Operating system and version
2. Python version: `python --version`
3. Package versions: `pip list | grep -E "(PyQt5|opencv|PIL|scenedetect)"`
4. FFmpeg version: `ffmpeg -version`
5. Error messages and log files
6. Steps to reproduce the issue

### Where to Get Help

1. Check this troubleshooting guide
2. Review project documentation in `docs/`
3. Search existing GitHub issues
4. Create a new GitHub issue with debug information

## Prevention Tips

### Best Practices

1. **Use virtual environments** to avoid dependency conflicts
2. **Keep dependencies updated** within compatible version ranges
3. **Regular backups** of your `~/.vchop/` settings directory
4. **Test with small video files** before processing large collections
5. **Monitor disk space** for thumbnail cache and output files

### System Requirements

- **Minimum RAM**: 2GB (4GB+ recommended for large video files)
- **Storage**: 1GB+ free space for thumbnails and temporary files
- **CPU**: Any modern processor (faster CPU improves scene detection speed)
- **Display**: Required for GUI (1024x768+ recommended)