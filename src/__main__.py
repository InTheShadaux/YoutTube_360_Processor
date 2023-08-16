import sys
import subprocess
import ffmpeg
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QFileDialog
from youtube_vr_utils import process_video
# from spatialmedia.metadata_utils import inject_metadata

class YouTubeVRApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube VR Metadata Uploader")

        self.process_button = QPushButton("Process Video", self)
        self.process_button.clicked.connect(self.process_video)

        self.output_folder_label = QLabel("Output Folder:", self)
        self.output_folder_input = QLineEdit(self)
        self.output_folder_button = QPushButton("Select Folder", self)
        self.output_folder_button.clicked.connect(self.select_output_folder)

        self.output_filename_label = QLabel("Output Filename:", self)
        self.output_filename_input = QLineEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(self.process_button)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_input)
        layout.addWidget(self.output_folder_button)
        layout.addWidget(self.output_filename_label)
        layout.addWidget(self.output_filename_input)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def process_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        input_file, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi);;All Files (*)", options=options)
        output_folder = self.output_folder_input.text()

        if input_file and output_folder:
            self.install_ffmpeg()  # Install FFmpeg if not available
            self.process_spatial_video(input_file, output_folder)
            self.output_folder_input.clear()

    def select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            self.output_folder_input.setText(output_folder)

    def install_ffmpeg(self):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ffmpeg-python"])
            print("FFmpeg installed successfully.")
        except subprocess.CalledProcessError:
            print("Error installing FFmpeg.")

    def process_spatial_video(self, input_file, output_folder):
        # output_file = os.path.join(output_folder, 'processed_' + os.path.basename(input_file))
        print(input_file)
        ffmpeg_output = output_folder + f"/ffmpeg_{os.path.basename(input_file)}"
        print(ffmpeg_output)
        (
            ffmpeg
            .input(input_file)
            .output(ffmpeg_output, vcodec='libx264', x264opts='frame-packing=3')
            .run()
        )

        # Inject 3D metadata using SpatialMedia
        subprocess.check_call([sys.executable, "spatialmedia", "-i", "--stereo=top-bottom", ffmpeg_output,  ffmpeg_output.replace("ffmpeg_", "processed_")])
        
        # print("Command execution result: ",proc.)
        print("Video processed and saved to:", ffmpeg_output, ffmpeg_output.replace("ffmpeg_", "processed_"))

def install_pyqt():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
        print("PyQt5 installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing PyQt5.")

def main():
    install_pyqt()  # Install PyQt5 if not available
    app = QApplication(sys.argv)
    window = YouTubeVRApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
