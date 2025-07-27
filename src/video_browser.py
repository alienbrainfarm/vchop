from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
import os
import subprocess
import json
from video_utils import VIDEO_EXTENSIONS, THUMBNAIL_SIZE, THUMBNAIL_DIR, load_recent_dirs, update_recent_dirs, clean_recent_dirs, is_video_file, create_thumbnail, convert_flv_to_mp4, RECENT_DIRS_PATH, get_thumbnail_path
from video_editor import VideoEditorWindow

class VideoBrowser(QMainWindow):
    def keyPressEvent(self, event):
        # Press 'j' to open join scenes editor from normal display
        if event.text() == 'j' and not hasattr(self, 'current_scene_files'):
            # Try to open the default scenes subdirectory if it exists
            base_dir = self.recent_dirs[0] if self.recent_dirs else os.getcwd()
            default_dir = os.path.join(base_dir, 'scenes')
            if os.path.exists(default_dir):
                self.show_scene_thumbnails(default_dir)
                return
        super().keyPressEvent(event)
    def eventFilter(self, source, event):
        # Handle '[' and ']' key for reordering when list_widget has focus
        if source is self.list_widget and event.type() == event.KeyPress:
            if hasattr(self, 'current_scene_files') and self.current_scene_files:
                selected = self.list_widget.currentRow()
                if selected == -1:
                    return False
                # Move up
                if event.text() == '[' and selected > 0:
                    self.current_scene_files[selected-1], self.current_scene_files[selected] = self.current_scene_files[selected], self.current_scene_files[selected-1]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    name = os.path.basename(self.current_scene_files[selected-1])
                    self.show_scene_thumbnails(self.current_scene_dir)
                    for i in range(self.list_widget.count()):
                        if self.list_widget.item(i).text() == name:
                            self.list_widget.setCurrentRow(i)
                            break
                    return True
                # Move down
                elif event.text() == ']' and selected < len(self.current_scene_files)-1:
                    self.current_scene_files[selected+1], self.current_scene_files[selected] = self.current_scene_files[selected], self.current_scene_files[selected+1]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    name = os.path.basename(self.current_scene_files[selected+1])
                    self.show_scene_thumbnails(self.current_scene_dir)
                    for i in range(self.list_widget.count()):
                        if self.list_widget.item(i).text() == name:
                            self.list_widget.setCurrentRow(i)
                            break
                    return True
                # Delete
                elif event.key() == Qt.Key_Delete:
                    file_to_delete = self.current_scene_files[selected]
                    # Use unified thumbnail cache location
                    thumb_dir = os.path.join(self.current_scene_dir, THUMBNAIL_DIR)
                    thumb_to_delete = get_thumbnail_path(file_to_delete, thumb_dir)
                    try:
                        if os.path.exists(file_to_delete):
                            os.remove(file_to_delete)
                        if os.path.exists(thumb_to_delete):
                            os.remove(thumb_to_delete)
                    except Exception:
                        pass
                    del self.current_scene_files[selected]
                    self.save_scene_order(self.current_scene_dir, self.current_scene_files)
                    self.show_scene_thumbnails(self.current_scene_dir)
                    # Select the next item if possible
                    if selected < len(self.current_scene_files):
                        self.list_widget.setCurrentRow(selected)
                    elif self.current_scene_files:
                        self.list_widget.setCurrentRow(len(self.current_scene_files)-1)
                    return True
        return super().eventFilter(source, event)
    def setup_scene_dragdrop(self):
        # Enable drag-and-drop reordering for the list_widget
        self.list_widget.setDragDropMode(self.list_widget.InternalMove)
        self.list_widget.model().rowsMoved.connect(self.on_scene_rows_moved)

    def on_scene_rows_moved(self, parent, start, end, dest, dest_row):
        # Update current_scene_files to match new order and save
        new_order = []
        for i in range(self.list_widget.count()):
            name = self.list_widget.item(i).text()
            for f in self.current_scene_files:
                if os.path.basename(f) == name:
                    new_order.append(f)
                    break
        self.current_scene_files = new_order
        self.save_scene_order(self.current_scene_dir, self.current_scene_files)
    def load_scene_order(self, dir_path, scene_files):
        order_file = os.path.join(dir_path, 'scene_order.txt')
        if os.path.exists(order_file):
            with open(order_file, 'r') as f:
                ordered_names = [line.strip() for line in f if line.strip()]
            # Only keep files that exist
            ordered_files = [os.path.join(dir_path, name) for name in ordered_names if os.path.join(dir_path, name) in scene_files]
            # Add any new files not in the order file at the end
            for f in scene_files:
                if f not in ordered_files:
                    ordered_files.append(f)
            return ordered_files
        else:
            # Default: sort by filename
            return sorted(scene_files)

    def save_scene_order(self, dir_path, scene_files):
        order_file = os.path.join(dir_path, 'scene_order.txt')
        with open(order_file, 'w') as f:
            for fpath in scene_files:
                f.write(f'{os.path.basename(fpath)}\n')

    def show_scene_thumbnails(self, dir_path):
        # Show all video files in dir_path as thumbnails in current list_widget, in order from order file if present
        from video_utils import is_video_file, get_thumbnail_path, create_thumbnail
        scene_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if is_video_file(f)]
        scene_files = self.load_scene_order(dir_path, scene_files)
        
        # Ensure thumbnail cache directory exists
        thumb_dir = os.path.join(dir_path, THUMBNAIL_DIR)
        os.makedirs(thumb_dir, exist_ok=True)
        
        self.list_widget.clear()
        for f in scene_files:
            # Use unified thumbnail cache directory and blue border for scene mode
            thumb_path = get_thumbnail_path(f, thumb_dir)
            if not os.path.exists(thumb_path):
                try:
                    create_thumbnail(f, thumb_path, border_color=(0, 0, 255))  # Blue border for scene mode
                except Exception:
                    pass
            
            if os.path.exists(thumb_path):
                pixmap = QPixmap(thumb_path)
            else:
                pixmap = QPixmap()
            item = QListWidgetItem(os.path.basename(f))
            item.setIcon(QIcon(pixmap))
            item.setSizeHint(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
            self.list_widget.addItem(item)
        # Store for later use
        self.current_scene_dir = dir_path
        self.current_scene_files = scene_files
        self.setup_scene_dragdrop()
        
        # Update window title to show scene editing mode
        self.setWindowTitle('vchop - Scene Editor')
        
        # Enable export functionality when in scene mode
        if hasattr(self, 'export_action'):
            self.export_action.setEnabled(True)

    def __init__(self, start_dir=None):
        super().__init__()
        self.setWindowTitle('vchop - Video Browser')
        self.setGeometry(100, 100, 800, 600)
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(10)
        self.list_widget.setStyleSheet('background-color: black;')
        self.setCentralWidget(self.list_widget)
        self.list_widget.itemDoubleClicked.connect(self.open_video_editor)
        self.list_widget.installEventFilter(self)
        self.recent_dirs = load_recent_dirs()
        self.create_menu()
        if start_dir:
            if os.path.exists(start_dir):
                self.open_directory(start_dir)
                self.recent_dirs = update_recent_dirs(start_dir, self.recent_dirs)
            else:
                QMessageBox.warning(self, 'Directory Not Found', 
                                  f'The specified directory does not exist:\n{start_dir}\n\n'
                                  f'Please select a valid directory.')
                self.select_directory()
        else:
            # Clean up recent_dirs to remove non-existent directories
            original_recent_dirs = self.recent_dirs
            self.recent_dirs = clean_recent_dirs(self.recent_dirs)
            # Save cleaned recent_dirs if any directories were removed
            if len(self.recent_dirs) != len(original_recent_dirs):
                RECENT_DIRS_PATH.parent.mkdir(parents=True, exist_ok=True)
                with open(RECENT_DIRS_PATH, 'w') as f:
                    json.dump(self.recent_dirs, f)
            
            if self.recent_dirs:
                # Try to open the most recent valid directory
                self.open_directory(self.recent_dirs[0])
            else:
                # No valid recent directories, prompt user to select one
                QMessageBox.information(self, 'No Recent Directories', 
                                      'No recent directories found or all previous directories no longer exist.\n\n'
                                      'Please select a directory to browse.')
                self.select_directory()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open Directory', self)
        open_action.triggered.connect(self.select_directory)
        file_menu.addAction(open_action)
        join_action = QAction('Join Scenes from Directory', self)
        join_action.triggered.connect(self.open_scene_manager_from_dir)
        file_menu.addAction(join_action)
        recent_menu = file_menu.addMenu('Recent Directories')
        for dir_path in self.recent_dirs:
            action = QAction(dir_path, self)
            action.triggered.connect(lambda checked, d=dir_path: self.open_directory(d))
            recent_menu.addAction(action)
        actions_menu = menubar.addMenu('Actions')
        split_action = QAction('Split by Scenes', self)
        split_action.triggered.connect(self.split_by_scenes)
        actions_menu.addAction(split_action)
        convert_action = QAction('Convert FLV to MP4', self)
        convert_action.triggered.connect(self.convert_flv_to_mp4)
        actions_menu.addAction(convert_action)
        
        # Store reference to export action for dynamic enabling/disabling
        self.export_action = QAction('Export Scenes to Video', self)
        self.export_action.triggered.connect(self.export_current_scenes)
        self.export_action.setEnabled(False)  # Initially disabled
        actions_menu.addAction(self.export_action)

    def open_scene_manager_from_dir(self):
        """Open scene manager to join videos from a directory."""
        # Default to subdirectory of current directory if possible
        base_dir = self.recent_dirs[0] if self.recent_dirs else os.getcwd()
        default_dir = os.path.join(base_dir, 'scenes')
        if not os.path.exists(default_dir):
            default_dir = base_dir
        
        # Show clear dialog message
        dir_path = QFileDialog.getExistingDirectory(
            self, 
            'Select Directory Containing Videos to Join Together', 
            default_dir
        )
        if not dir_path:
            QMessageBox.information(self, 'No Directory Selected', 
                                  'No directory was selected. Please select a directory containing videos to join.')
            return
            
        from video_utils import is_video_file
        scene_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if is_video_file(f)]
        
        if not scene_files:
            QMessageBox.warning(self, 'No Videos Found', 
                              f'No video files found in selected directory:\n{dir_path}\n\n'
                              f'Please select a directory that contains video files to join.')
            return
            
        QMessageBox.information(self, 'Videos Found', 
                              f'Found {len(scene_files)} video file(s) in:\n{dir_path}\n\n'
                              f'You can now reorder the videos by dragging them and then export to a single joined video.')
        
        self.show_scene_thumbnails(dir_path)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.open_directory(dir_path)
            self.recent_dirs = update_recent_dirs(dir_path, self.recent_dirs)

    def open_directory(self, dir_path):
        if not os.path.exists(dir_path):
            QMessageBox.warning(self, 'Directory Not Found', 
                              f'The directory does not exist:\n{dir_path}\n\n'
                              f'Please select a valid directory.')
            self.select_directory()
            return
            
        # Reset window title to browser mode and clear scene mode state
        self.setWindowTitle('vchop - Video Browser')
        if hasattr(self, 'current_scene_files'):
            delattr(self, 'current_scene_files')
        if hasattr(self, 'current_scene_dir'):
            delattr(self, 'current_scene_dir')
        if hasattr(self, 'export_action'):
            self.export_action.setEnabled(False)
            
        self.list_widget.clear()
        thumb_dir = os.path.join(dir_path, THUMBNAIL_DIR)
        os.makedirs(thumb_dir, exist_ok=True)
        for filename in os.listdir(dir_path):
            if is_video_file(filename):
                filepath = os.path.join(dir_path, filename)
                thumb_path = os.path.join(thumb_dir, f'{filename}.png')
                if not os.path.exists(thumb_path):
                    try:
                        create_thumbnail(filepath, thumb_path)
                    except Exception:
                        thumb_path = None
                if os.path.exists(thumb_path):
                    pixmap = QPixmap(thumb_path)
                else:
                    pixmap = QPixmap()
                item = QListWidgetItem(filename)
                item.setIcon(QIcon(pixmap))
                item.setSizeHint(QSize(THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
                self.list_widget.addItem(item)

    def open_video_editor(self, item):
        dir_path = self.recent_dirs[0] if self.recent_dirs else None
        if not dir_path:
            QMessageBox.warning(self, 'No Directory', 'No directory found for editing.')
            return
        video_path = os.path.join(dir_path, item.text())
        self.editor = VideoEditorWindow(video_path, self)
        self.editor.show()

    def split_by_scenes(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select a video to split by scenes.')
            return
        filename = selected_items[0].text()
        dir_path = self.recent_dirs[0] if self.recent_dirs else None
        if not dir_path:
            QMessageBox.warning(self, 'No Directory', 'No directory found for splitting.')
            return
        video_path = os.path.join(dir_path, filename)
        self.editor = VideoEditorWindow(video_path, self)
        self.editor.show()

    def convert_flv_to_mp4(self):
        """Convert selected FLV files to MP4 format."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select FLV files to convert to MP4.')
            return
        
        dir_path = self.recent_dirs[0] if self.recent_dirs else None
        if not dir_path:
            QMessageBox.warning(self, 'No Directory', 'No directory found for conversion.')
            return
        
        flv_files = []
        for item in selected_items:
            filename = item.text()
            if filename.lower().endswith('.flv'):
                flv_files.append(os.path.join(dir_path, filename))
        
        if not flv_files:
            QMessageBox.warning(self, 'No FLV Files', 'No FLV files selected. Please select FLV files to convert.')
            return
        
        converted_count = 0
        for flv_path in flv_files:
            try:
                mp4_path = convert_flv_to_mp4(flv_path)
                if mp4_path:
                    converted_count += 1
                    # Create thumbnail for the new MP4 file
                    thumb_dir = os.path.join(dir_path, THUMBNAIL_DIR)
                    thumb_path = os.path.join(thumb_dir, f'{os.path.basename(mp4_path)}.png')
                    create_thumbnail(mp4_path, thumb_path)
                else:
                    print(f"Failed to convert {flv_path}")
            except Exception as e:
                print(f"Error converting {flv_path}: {e}")
        
        if converted_count > 0:
            QMessageBox.information(self, 'Conversion Complete', 
                                  f'Successfully converted {converted_count} FLV file(s) to MP4.')
            # Refresh the directory view to show new MP4 files
            self.open_directory(dir_path)
        else:
            QMessageBox.warning(self, 'Conversion Failed', 'Failed to convert any FLV files.')


    def export_current_scenes(self):
        """Export currently displayed scenes to a single video file."""
        if not hasattr(self, 'current_scene_files') or not self.current_scene_files:
            QMessageBox.warning(self, 'No Scenes', 'No scenes available to export. Please open a directory with video files first.')
            return
            
        output_file, _ = QFileDialog.getSaveFileName(
            self, 
            'Save Joined Video', 
            '', 
            'MP4 Files (*.mp4)'
        )
        if not output_file:
            QMessageBox.information(self, 'Export Cancelled', 'Export was cancelled.')
            return
            
        try:
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                concat_file = os.path.join(tmpdir, 'concat.txt')
                with open(concat_file, 'w') as f:
                    for scene_file in self.current_scene_files:
                        # Use absolute paths and escape single quotes
                        safe_path = scene_file.replace("'", "'\"'\"'")
                        f.write(f"file '{safe_path}'\n")
                
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', concat_file,
                    '-c', 'copy',
                    output_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    QMessageBox.information(self, 'Export Complete', 
                                          f'Successfully joined {len(self.current_scene_files)} videos to:\n{output_file}')
                else:
                    QMessageBox.warning(self, 'Export Failed', 
                                      f'Failed to export video. Error:\n{result.stderr}')
                    
        except Exception as e:
            QMessageBox.warning(self, 'Export Error', f'An error occurred during export:\n{str(e)}')
