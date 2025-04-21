import yt_dlp

class YouTubeExtractor:
    def __init__(self, url):
        self.url = url

    async def extract_info(self):
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forcejson": True,
            "extract_flat": False,
            "cookiefile": "cookies/cookies.txt",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                return info
        except Exception as e:
            print(f"[Extractor] Error extracting info: {str(e)}")
            return None
