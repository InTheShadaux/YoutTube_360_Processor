import ffmpeg
import os

def process_video(input_file, output_folder):
    output_file = os.path.join(output_folder, 'processed_' + os.path.basename(input_file))
    ffmpeg.input(input_file).output(output_file, vcodec='libx264', x264opts='frame-packing=3', metadata={
        'stereo_mode': 'side_by_side',  # Adjust this to the appropriate 3D mode
    }).run()
    print("Video processed and saved to:", output_file)

