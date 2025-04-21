class FormatSelector:
    def __init__(self, video_info):
        self.formats = video_info.get("formats", [])

    def select_format(self, quality="best"):
        if quality == "best":
            return self.formats[0] if self.formats else None

        # Match by audio bitrate like "128k"
        if quality.endswith("k"):
            target_abr = int(quality.replace("k", ""))
            for fmt in self.formats:
                abr = fmt.get("abr")
                if abr and abs(int(abr) - target_abr * 1000) <= 1000:
                    return fmt

        # Match by video resolution like "720p"
        if "p" in quality:
            for fmt in self.formats:
                if fmt.get("resolution") == quality:
                    return fmt

        return None
