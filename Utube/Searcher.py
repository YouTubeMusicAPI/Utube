from YouTubeMusic.YtSearch import Search

class YouTubeSearcher:
    @staticmethod
    async def search(query: str, limit=1):
        try:
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
        except Exception as e:
            print(f"[Searcher] Error searching YouTube: {e}")
            return None
