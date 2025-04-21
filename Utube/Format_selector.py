class FormatSelector:
    def __init__(self, video_info):
        self.video_info = video_info

    def select_format(self, quality):
        available_formats = self.video_info.get("formats", [])
        
        # First try to find the exact match for quality
        for fmt in available_formats:
            if quality in [fmt.get("abr", ""), fmt.get("resolution", "")]:
                return fmt

        # Fallback: select the highest available quality format
        for fmt in available_formats:
            if fmt.get("abr"):  # for audio, prioritize by bitrate
                return fmt
            if fmt.get("resolution"):  # for video, prioritize by resolution
                return fmt
        
        return None  # No matching format found
