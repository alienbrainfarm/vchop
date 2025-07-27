import unittest
import tempfile
import os
import subprocess
from unittest.mock import patch, MagicMock
from src.video_utils import convert_flv_to_mp4

class TestFFmpegErrorHandling(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.flv_path = os.path.join(self.test_dir, 'test.flv')
        self.mp4_path = os.path.join(self.test_dir, 'test.mp4')
        
        # Create a dummy FLV file
        with open(self.flv_path, 'wb') as f:
            f.write(b'dummy flv content')
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_ffmpeg_preferred_over_opencv(self):
        """Test that FFmpeg is preferred over OpenCV by default."""
        with patch('src.video_utils.subprocess.run') as mock_run:
            # Mock successful FFmpeg call
            mock_run.return_value.returncode = 0
            
            # Mock os.path.exists to return True for the output file
            with patch('src.video_utils.os.path.exists') as mock_exists:
                mock_exists.return_value = True
                
                result = convert_flv_to_mp4(self.flv_path, self.mp4_path)
                
                # Verify FFmpeg was called
                mock_run.assert_called_once()
                call_args = mock_run.call_args[0][0]
                self.assertEqual(call_args[0], 'ffmpeg')
                self.assertIn('-i', call_args)
                self.assertIn(self.flv_path, call_args)
                self.assertIn(self.mp4_path, call_args)
                
                self.assertEqual(result, self.mp4_path)
    
    def test_ffmpeg_not_found_fallback(self):
        """Test fallback to OpenCV when FFmpeg is not found."""
        with patch('src.video_utils.subprocess.run') as mock_run:
            # Mock FFmpeg not found
            mock_run.side_effect = FileNotFoundError("ffmpeg not found")
            
            # Mock OpenCV conversion
            with patch('src.video_utils.convert_flv_to_mp4_opencv') as mock_opencv:
                mock_opencv.return_value = self.mp4_path
                
                result = convert_flv_to_mp4(self.flv_path, self.mp4_path)
                
                # Verify FFmpeg was attempted
                mock_run.assert_called_once()
                
                # Verify OpenCV fallback was called
                mock_opencv.assert_called_once_with(self.flv_path, self.mp4_path)
                
                self.assertEqual(result, self.mp4_path)
    
    def test_ffmpeg_failure_fallback(self):
        """Test fallback to OpenCV when FFmpeg fails."""
        with patch('src.video_utils.subprocess.run') as mock_run:
            # Mock FFmpeg failure
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stderr = "FFmpeg error message"
            mock_run.return_value = mock_result
            
            # Mock OpenCV conversion
            with patch('src.video_utils.convert_flv_to_mp4_opencv') as mock_opencv:
                mock_opencv.return_value = self.mp4_path
                
                result = convert_flv_to_mp4(self.flv_path, self.mp4_path)
                
                # Verify FFmpeg was attempted
                mock_run.assert_called_once()
                
                # Verify OpenCV fallback was called
                mock_opencv.assert_called_once_with(self.flv_path, self.mp4_path)
                
                self.assertEqual(result, self.mp4_path)
    
    def test_use_opencv_parameter(self):
        """Test that use_opencv=True bypasses FFmpeg."""
        with patch('src.video_utils.subprocess.run') as mock_run:
            # Mock OpenCV conversion
            with patch('src.video_utils.convert_flv_to_mp4_opencv') as mock_opencv:
                mock_opencv.return_value = self.mp4_path
                
                result = convert_flv_to_mp4(self.flv_path, self.mp4_path, use_opencv=True)
                
                # Verify FFmpeg was NOT called
                mock_run.assert_not_called()
                
                # Verify OpenCV was called directly
                mock_opencv.assert_called_once_with(self.flv_path, self.mp4_path)
                
                self.assertEqual(result, self.mp4_path)

if __name__ == '__main__':
    unittest.main()