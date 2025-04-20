import subprocess
import os

class PostProcessor:
    def __init__(self, video_filename):
        self.video_filename = video_filename

    async def convert_to_mp3(self):
        output_filename = f"{os.path.splitext(self.video_filename)[0]}.mp3"
        command = ['ffmpeg', '-i', self.video_filename, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', output_filename]
        
        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted to MP3: {output_filename}")
            return output_filename
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return None
