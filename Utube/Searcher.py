import asyncio
from YouTubeMusic.YtSearch import Search

class YTSearcher:
    @staticmethod
    async def search(query: str, limit=1):
        results = await Search(query, limit=limit)
        if not results:
            return None
        songs = []
        for song in results:
            songs.append({
                "title": song.get("title"),
                "url": song.get("url"),
                "thumbnail": song.get("thumbnail"),
                "channel": song.get("channel_name"),
                "views": song.get("views"),
                "duration": song.get("duration"),
                "artist": song.get("artist_name"),
                "description": song.get("description")
            })
        return songs
      
