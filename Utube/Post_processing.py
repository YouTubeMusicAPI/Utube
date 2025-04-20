import subprocess
import os

class PostProcessor:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_to_mp3(self):
        output_file = self.input_file.rsplit('.', 1)[0] + ".mp3"
        command = [
            "ffmpeg",
            "-i", self.input_file,
            "-vn",
            "-ab", "192k",
            "-ar", "44100",
            "-y",
            output_file
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(output_file):
            return output_file
        return None
