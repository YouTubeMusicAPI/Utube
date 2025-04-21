class FormatSelector:
    def __init__(self, video_info):
        self.formats = video_info.get("formats", [])

    def select_format(self, quality="best"):
        if not self.formats:
            return None

        # Normalize and sort formats based on available fields
        def quality_score(fmt):
            if "resolution" in fmt:
                res = fmt["resolution"].replace("p", "")
                return int(res) if res.isdigit() else 0
            elif "abr" in fmt:
                return int(fmt["abr"])  # audio bitrate
            return 0

        # Sort by highest quality first
        sorted_formats = sorted(self.formats, key=quality_score, reverse=True)

        # Debug: print what we're trying to match
        print(f"\n🔍 Looking for quality: {quality}")
        print(f"🔢 Sorted Formats by Quality Score:")
        for fmt in sorted_formats:
            print(fmt)

        # If quality is 'best', return the top format
        if quality == "best":
            return sorted_formats[0]

        # If it's an audio quality like '128k'
        if quality.endswith("k"):
            try:
                target_kbps = int(quality.replace("k", ""))
                for fmt in sorted_formats:
                    if "abr" in fmt and abs(int(fmt["abr"] / 1000) - target_kbps) <= 8:
                        return fmt
            except Exception as e:
                print(f"Error matching abr: {e}")

        # If it's a video resolution like '720p'
        if quality.endswith("p"):
            for fmt in sorted_formats:
                if fmt.get("resolution") == quality:
                    return fmt

        return None
