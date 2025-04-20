from youtubesearchpython import VideosSearch

class YouTubeSearcher:
    async def search(self, query):
        try:
            search = VideosSearch(query, limit=5)
            results = await search.next()
            videos = []

            for video in results.get("result", []):
                videos.append({
                    "title": video.get("title"),
                    "url": video.get("link"),
                    "duration": video.get("duration"),
                    "channel": video.get("channel", {}).get("name"),
                    "views": video.get("viewCount", {}).get("short"),
                })

            return videos

        except Exception as e:
            print(f"[Searcher] Error searching YouTube: {str(e)}")
            return []
