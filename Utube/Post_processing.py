import asyncio
import os
import subprocess

class PostProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file.rsplit(".", 1)[0] + ".mp3"

    async def convert_to_mp3(self):
        print(f"[PostProcessor] Converting {self.input_file} to MP3")

        if not os.path.exists(self.input_file):
            print(f"[PostProcessor] Input file not found: {self.input_file}")
            return None

        cmd = [
            "ffmpeg", "-y",
            "-i", self.input_file,
            "-vn",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",
            self.output_file
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"[PostProcessor] ffmpeg error:\n{stderr.decode()}")
                return None

            print(f"[PostProcessor] Conversion completed: {self.output_file}")
            return self.output_file

        except Exception as e:
            print(f"[PostProcessor] Exception during conversion: {str(e)}")
            return None
