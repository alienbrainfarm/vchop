
import sys
from PyQt5.QtWidgets import QApplication
from video_browser import VideoBrowser

def main():
    start_dir = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    window = VideoBrowser(start_dir)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
