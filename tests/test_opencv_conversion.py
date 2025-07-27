import unittest
import os
import tempfile
from src.video_utils import convert_flv_to_mp4_opencv, convert_flv_to_mp4

class TestOpenCVConversion(unittest.TestCase):
    
    def setUp(self):
        """Create a test FLV file for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.flv_path = os.path.join(self.test_dir, 'test.flv')
        
        # Create a simple test FLV file using OpenCV
        import cv2
        import numpy as np
        fourcc = cv2.VideoWriter_fourcc(*'FLV1')
        out = cv2.VideoWriter(self.flv_path, fourcc, 1.0, (64, 64))
        
        # Write a few frames
        for i in range(5):
            frame = np.full((64, 64, 3), i * 50, dtype=np.uint8)
            out.write(frame)
        out.release()
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_opencv_conversion(self):
        """Test OpenCV-based FLV to MP4 conversion."""
        mp4_path = convert_flv_to_mp4_opencv(self.flv_path)
        
        self.assertIsNotNone(mp4_path)
        self.assertTrue(mp4_path.endswith('.mp4'))
        self.assertTrue(os.path.exists(mp4_path))
        self.assertGreater(os.path.getsize(mp4_path), 0)
    
    def test_hybrid_conversion_opencv_preferred(self):
        """Test that the hybrid function can use OpenCV when explicitly requested."""
        mp4_path = convert_flv_to_mp4(self.flv_path, use_opencv=True)
        
        self.assertIsNotNone(mp4_path)
        self.assertTrue(mp4_path.endswith('.mp4'))
        self.assertTrue(os.path.exists(mp4_path))
    
    def test_conversion_with_invalid_file(self):
        """Test conversion with non-existent file."""
        result = convert_flv_to_mp4_opencv('/nonexistent/file.flv')
        self.assertIsNone(result)
    
    def test_conversion_with_non_flv_file(self):
        """Test conversion with non-FLV file."""
        txt_path = os.path.join(self.test_dir, 'test.txt')
        with open(txt_path, 'w') as f:
            f.write('not a video file')
        
        result = convert_flv_to_mp4_opencv(txt_path)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()