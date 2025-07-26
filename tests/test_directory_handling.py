import unittest
import os
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from video_utils import clean_recent_dirs, load_recent_dirs, update_recent_dirs, RECENT_DIRS_PATH

class TestDirectoryHandling(unittest.TestCase):
    
    def test_clean_recent_dirs_removes_nonexistent(self):
        """Test that clean_recent_dirs removes non-existent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            existing_dir = tmpdir
            nonexistent_dir = os.path.join(tmpdir, 'nonexistent')
            
            recent_dirs = [existing_dir, nonexistent_dir]
            cleaned = clean_recent_dirs(recent_dirs)
            
            self.assertEqual(len(cleaned), 1)
            self.assertIn(existing_dir, cleaned)
            self.assertNotIn(nonexistent_dir, cleaned)
    
    def test_clean_recent_dirs_empty_list(self):
        """Test that clean_recent_dirs handles empty list."""
        cleaned = clean_recent_dirs([])
        self.assertEqual(cleaned, [])
    
    def test_clean_recent_dirs_all_exist(self):
        """Test that clean_recent_dirs preserves all existing directories."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                recent_dirs = [tmpdir1, tmpdir2]
                cleaned = clean_recent_dirs(recent_dirs)
                
                self.assertEqual(len(cleaned), 2)
                self.assertEqual(set(cleaned), set(recent_dirs))
    
    def test_clean_recent_dirs_all_nonexistent(self):
        """Test that clean_recent_dirs removes all non-existent directories."""
        recent_dirs = ['/nonexistent1', '/nonexistent2']
        cleaned = clean_recent_dirs(recent_dirs)
        self.assertEqual(cleaned, [])

    def test_recent_dirs_persistence(self):
        """Test that recent directories are properly saved and loaded."""
        # Use a temporary file for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            test_recent_path = Path(tmpdir) / 'test_recent_dirs.json'
            
            # Temporarily override the path
            original_path = RECENT_DIRS_PATH
            import video_utils
            video_utils.RECENT_DIRS_PATH = test_recent_path
            
            try:
                # Test with a real directory
                test_dirs = [tmpdir]
                test_recent_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(test_recent_path, 'w') as f:
                    json.dump(test_dirs, f)
                
                loaded_dirs = load_recent_dirs()
                self.assertEqual(loaded_dirs, test_dirs)
                
            finally:
                # Restore original path
                video_utils.RECENT_DIRS_PATH = original_path

if __name__ == '__main__':
    unittest.main()