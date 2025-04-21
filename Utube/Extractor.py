import aiohttp
import re
import json

class YouTubeExtractor:
    def __init__(self, url):
        self.url = url

    async def extract_info(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                html = await resp.text()
                
        # Extract `ytInitialPlayerResponse` JSON from HTML
        data = self._extract_json(html)
        if not data:
            return None

        return self._parse_streams(data)

    def _extract_json(self, html):
        try:
            match = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.*?\});", html)
            if match:
                return json.loads(match.group(1))
        except Exception as e:
            print(f"Error parsing ytInitialPlayerResponse: {e}")
        return None

    def _parse_streams(self, data):
        video_details = data.get("videoDetails", {})
        streaming_data = data.get("streamingData", {})

        formats = streaming_data.get("formats", []) + streaming_data.get("adaptiveFormats", [])

        stream_list = []
        for f in formats:
            stream_list.append({
                "url": f.get("url"),
                "mimeType": f.get("mimeType"),
                "quality": f.get("qualityLabel") or f.get("audioQuality"),
                "bitrate": f.get("bitrate"),
                "abr": f.get("averageBitrate"),
                "format": f.get("mimeType").split(";")[0] if f.get("mimeType") else "unknown",
            })

        return {
            "title": video_details.get("title"),
            "duration": video_details.get("lengthSeconds"),
            "author": video_details.get("author"),
            "formats": stream_list
        }
