import sys
import subprocess
import ffmpeg
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QFileDialog, QMessageBox

class YouTubeVRApp(QMainWindow):
    # Initialize the application
    def __init__(self):
        super().__init__()

        self.init_ui()

    # Initialize the UI
    def init_ui(self):
        self.setWindowTitle("YouTube VR Metadata Uploader")

        self.process_button = QPushButton("Process Video", self)
        self.process_button.clicked.connect(self.process_video)

        self.output_folder_label = QLabel("Output Folder:", self)
        self.output_folder_input = QLineEdit(self)
        self.output_folder_button = QPushButton("Select Folder", self)
        self.output_folder_button.clicked.connect(self.select_output_folder)


        layout = QVBoxLayout()
        layout.addWidget(self.process_button)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_input)
        layout.addWidget(self.output_folder_button)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Process the video
    def process_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        input_file, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi);;All Files (*)", options=options)
        output_folder = self.output_folder_input.text()

        if input_file and output_folder:
            self.process_spatial_video(input_file, output_folder)
            self.output_folder_input.clear()
            
    # Select the output folder
    def select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            self.output_folder_input.setText(output_folder)

    # Process the video using FFmpeg and SpatialMedia
    def process_spatial_video(self, input_file, output_folder):
        print(input_file)
        ffmpeg_output = output_folder + f"/ffmpeg_{os.path.basename(input_file)}"
        print(ffmpeg_output)
        #Print that the file is being processed in FFmpeg
        print("Processing file in FFmpeg...")
        (
            ffmpeg
            .input(input_file)
            .output(ffmpeg_output, vcodec='libx264', x264opts='frame-packing=3')
            .run()
        )
        #Print that the file has finished processing in FFmpeg
        print("File has finished processing in FFmpeg. Moving to SpatialMedia...")

        # Get the current working directory
        cwd = os.getcwd()

        # Get the path to the spatialmedia directory which is under the parent directory
        spatialmedia = os.path.join(cwd, "spatialmedia")

        # Inject 3D metadata using SpatialMedia and rename file
        subprocess.check_call([sys.executable, spatialmedia, "-i", "--stereo=top-bottom", ffmpeg_output,  ffmpeg_output.replace("ffmpeg_", "processed_")])

        #Print that the file has finished processing in SpatialMedia
        print("File has finished processing in SpatialMedia...")

        # Delete original FFmpeg output
        os.remove(ffmpeg_output)

        #Print that the file has been deleted
        print("Original FFmpeg output has been deleted...")

# Run the application
def main():
    app = QApplication(sys.argv)
    window = YouTubeVRApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
