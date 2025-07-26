import unittest
import tempfile
import os
from src.video_utils import create_thumbnail

class TestThumbnailBorders(unittest.TestCase):
    
    def setUp(self):
        """Create a test video file for thumbnail testing."""
        self.test_dir = tempfile.mkdtemp()
        self.video_path = os.path.join(self.test_dir, 'test_video.mp4')
        self.thumb_path = os.path.join(self.test_dir, 'thumbnail.png')
        
        # Create a simple test video using OpenCV
        import cv2
        import numpy as np
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.video_path, fourcc, 1.0, (64, 64))
        
        # Write a few black frames
        for _ in range(3):
            frame = np.zeros((64, 64, 3), dtype=np.uint8)
            out.write(frame)
        out.release()
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_thumbnail_creation_with_border(self):
        """Test that thumbnail is created with yellow border."""
        result = create_thumbnail(self.video_path, self.thumb_path)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.thumb_path))
        
        # Check that the thumbnail has the expected size
        from PIL import Image
        img = Image.open(self.thumb_path)
        self.assertEqual(img.size, (200, 200))  # THUMBNAIL_SIZE
        
        # Check that the corners are yellow (border color)
        # Get pixel at corner - should be yellow
        corner_pixel = img.getpixel((0, 0))
        self.assertEqual(corner_pixel, (255, 255, 0))  # Yellow RGB
        
        # Check that there's a black area inside (inner background)
        # Get pixel that should be in the inner black area
        inner_pixel = img.getpixel((10, 10))  # Inside the border
        self.assertEqual(inner_pixel, (0, 0, 0))  # Black RGB
    
    def test_thumbnail_border_width(self):
        """Test that the border has the expected width."""
        result = create_thumbnail(self.video_path, self.thumb_path)
        self.assertTrue(result)
        
        from PIL import Image
        img = Image.open(self.thumb_path)
        
        # Check border pixels (should be yellow)
        for i in range(3):  # Border width is 3
            # Top edge
            self.assertEqual(img.getpixel((50, i)), (255, 255, 0))
            # Left edge  
            self.assertEqual(img.getpixel((i, 50)), (255, 255, 0))
            # Right edge
            self.assertEqual(img.getpixel((199-i, 50)), (255, 255, 0))
            # Bottom edge
            self.assertEqual(img.getpixel((50, 199-i)), (255, 255, 0))

if __name__ == '__main__':
    unittest.main()