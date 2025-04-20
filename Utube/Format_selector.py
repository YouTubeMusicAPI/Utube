class FormatSelector:
    def __init__(self, video_info):
        self.formats = video_info.get("formats", [])

    def select_format(self, quality):
        if not self.formats:
            return None

        if "k" in quality:  # audio quality like 128k, 192k
            bitrate = int(quality.replace("k", ""))
            for f in sorted(self.formats, key=lambda x: int(x.get("abr", 0)), reverse=True):
                if f.get("vcodec") == "none" and int(f.get("abr", 0)) <= bitrate:
                    return {
                        "url": f["url"],
                        "format": f["ext"],
                        "resolution": f"{f.get('abr', 'audio')}k"
                    }
        else:
            for f in sorted(self.formats, key=lambda x: int(x.get("height", 0)), reverse=True):
                if f.get("acodec") != "none" and f.get("vcodec") != "none":
                    return {
                        "url": f["url"],
                        "format": f["ext"],
                        "resolution": f"{f.get('height')}p"
                    }

        return None
