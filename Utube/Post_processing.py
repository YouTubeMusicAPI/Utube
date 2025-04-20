import shlex

class PostProcessor:
    def __init__(self, filename):
        self.filename = filename

    async def convert_to_mp3(self):
        import subprocess
        import os
        
        quoted_filename = shlex.quote(self.filename)
        output_filename = quoted_filename.replace(".mp4", ".mp3")

        cmd = f"ffmpeg -i {quoted_filename} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {shlex.quote(output_filename)}"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            return output_filename
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return None
