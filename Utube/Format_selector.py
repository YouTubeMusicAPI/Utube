class FormatSelector:
    def __init__(self, video_info):
        self.formats = video_info.get("formats", [])

    def select_format(self, quality="best"):
        # Filter out None or invalid abr values
        valid_formats = [f for f in self.formats if f.get("abr") is not None]

        if not valid_formats:
            return None

        try:
            sorted_formats = sorted(valid_formats, key=lambda x: int(float(x["abr"])), reverse=True)
        except Exception as e:
            print(f"[FormatSelector] Error while sorting formats: {e}")
            return None

        if quality.endswith("k"):
            # Convert "128k" -> 128
            try:
                target_abr = int(quality.replace("k", ""))
                for fmt in sorted_formats:
                    if int(float(fmt["abr"])) == target_abr:
                        return fmt
            except Exception as e:
                print(f"[FormatSelector] Error selecting specific quality: {e}")

        return sorted_formats[0] if sorted_formats else None
