import unittest
import os
from src.main import VideoBrowser, VIDEO_EXTENSIONS
from PyQt5.QtWidgets import QApplication
import sys

class TestVideoBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def test_open_directory_lists_videos(self):
        # Create a temporary directory with dummy video files
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdirname:
            filenames = ['test1.mp4', 'test2.avi', 'not_video.txt']
            for fname in filenames:
                open(os.path.join(tmpdirname, fname), 'a').close()
            browser = VideoBrowser()
            browser.open_directory(tmpdirname)
            listed = [browser.list_widget.item(i).text() for i in range(browser.list_widget.count())]
            self.assertIn('test1.mp4', listed)
            self.assertIn('test2.avi', listed)
            self.assertNotIn('not_video.txt', listed)

if __name__ == '__main__':
    unittest.main()
