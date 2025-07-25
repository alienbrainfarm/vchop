import unittest
import os
from src.video_utils import is_video_file, create_thumbnail, convert_flv_to_mp4
import tempfile

class TestVideoUtils(unittest.TestCase):
    def test_is_video_file(self):
        self.assertTrue(is_video_file('movie.mp4'))
        self.assertTrue(is_video_file('clip.AVI'))
        self.assertFalse(is_video_file('document.txt'))

    def test_create_thumbnail(self):
        # Create a dummy black video using OpenCV
        import cv2
        video_path = os.path.join(tempfile.gettempdir(), 'test_video.mp4')
        thumb_path = os.path.join(tempfile.gettempdir(), 'test_thumb.png')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 1.0, (64, 64))
        import numpy as np
        for _ in range(5):
            frame = np.zeros((64, 64, 3), dtype=np.uint8)
            out.write(frame)
        out.release()
        result = create_thumbnail(video_path, thumb_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(thumb_path))
        os.remove(video_path)
        os.remove(thumb_path)

    def test_convert_flv_to_mp4(self):
        # Test with the sample FLV file we created
        flv_path = '/tmp/vchop_test/test.flv'
        if os.path.exists(flv_path):
            mp4_path = convert_flv_to_mp4(flv_path)
            self.assertIsNotNone(mp4_path)
            self.assertTrue(mp4_path.endswith('.mp4'))
            self.assertTrue(os.path.exists(mp4_path))
            # Clean up
            if os.path.exists(mp4_path):
                os.remove(mp4_path)
        
        # Test with non-existent file
        result = convert_flv_to_mp4('/nonexistent/file.flv')
        self.assertIsNone(result)
        
        # Test with non-FLV file
        result = convert_flv_to_mp4('/tmp/notflv.txt')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
