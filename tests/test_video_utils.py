import unittest
import os
from src.video_utils import is_video_file, create_thumbnail
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

if __name__ == '__main__':
    unittest.main()
