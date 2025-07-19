
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from video_utils import VIDEO_EXTENSIONS

class TestVideoExtensions(unittest.TestCase):
    def test_video_extensions(self):
        self.assertIn('.mp4', VIDEO_EXTENSIONS)
        self.assertIn('.avi', VIDEO_EXTENSIONS)
        self.assertIn('.mov', VIDEO_EXTENSIONS)

if __name__ == '__main__':
    unittest.main()
