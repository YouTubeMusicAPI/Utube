class FormatSelector:
    def __init__(self, video_info):
        self.video_info = video_info

    def select_format(self, quality="best"):
        formats = self.video_info['formats']

        if quality == "best":
            return max(formats, key=lambda x: x['quality'])

        elif quality == "audio":
            return next((f for f in formats if f['format'] == 'audio/mp3'), None)

        elif quality == "4k":
            return next((f for f in formats if f['resolution'] == '2160p (4K)'), None)

        elif quality == "1440p":
            return next((f for f in formats if f['resolution'] == '1440p'), None)

        elif quality == "1080p":
            return next((f for f in formats if f['resolution'] == '1080p'), None)

        elif quality == "720p":
            return next((f for f in formats if f['resolution'] == '720p'), None)

        elif quality == "480p":
            return next((f for f in formats if f['resolution'] == '480p'), None)

        return max(formats, key=lambda x: x['quality'])
