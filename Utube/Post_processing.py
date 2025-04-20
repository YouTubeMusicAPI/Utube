import shlex
import os
import subprocess

class PostProcessor:
    def __init__(self, filename):
        self.filename = filename

    async def convert_to_mp3(self):
        if not os.path.exists(self.filename):
            print(f"File not found: {self.filename}")
            return None

        quoted_filename = shlex.quote(self.filename)
        output_filename = quoted_filename.replace(".mp4", ".mp3")

        cmd = f"ffmpeg -i {quoted_filename} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {shlex.quote(output_filename)}"

        try:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())  # Print ffmpeg output
            return output_filename
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e.stderr.decode()}")  # Print error output
            return None
