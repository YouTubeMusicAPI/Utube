import requests
from bs4 import BeautifulSoup

class YouTubeExtractor:
    def __init__(self, url):
        self.url = url
        self.page = self._fetch_page()

    def _fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def extract_info(self):
        if not self.page:
            return None

        soup = BeautifulSoup(self.page, 'html.parser')
        title_tag = soup.find('meta', {'name': 'title'})
        video_tag = soup.find('link', {'rel': 'canonical'})

        if not title_tag or not video_tag:
            return None

        title = title_tag['content']
        video_url = video_tag['href']
        formats = self._extract_formats()

        return {'title': title, 'video_url': video_url, 'formats': formats}

    def _extract_formats(self):
        formats = [
            {'quality': 2160, 'resolution': '2160p (4K)', 'url': 'https://example.com/video_url_2160p', 'format': 'video/mp4'},
            {'quality': 1440, 'resolution': '1440p', 'url': 'https://example.com/video_url_1440p', 'format': 'video/mp4'},
            {'quality': 1080, 'resolution': '1080p', 'url': 'https://example.com/video_url_1080p', 'format': 'video/mp4'},
            {'quality': 720, 'resolution': '720p', 'url': 'https://example.com/video_url_720p', 'format': 'video/mp4'},
            {'quality': 480, 'resolution': '480p', 'url': 'https://example.com/video_url_480p', 'format': 'video/mp4'},
            {'quality': 320, 'resolution': 'audio-only', 'url': 'https://example.com/audio_url_320kbps', 'format': 'audio/mp3'}
        ]
        return formats
      
