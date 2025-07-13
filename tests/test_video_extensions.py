import unittest
import os
from src.main import VIDEO_EXTENSIONS

class TestVideoExtensions(unittest.TestCase):
    def test_video_extensions(self):
        self.assertIn('.mp4', VIDEO_EXTENSIONS)
        self.assertIn('.avi', VIDEO_EXTENSIONS)
        self.assertIn('.mov', VIDEO_EXTENSIONS)

if __name__ == '__main__':
    unittest.main()
