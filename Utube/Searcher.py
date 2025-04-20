from youtubesearchpython import VideosSearch

class YouTubeSearcher:
    async def search(self, query):
        try:
            videos_search = VideosSearch(query, limit=1)
            result = await videos_search.next()
            video_list = result.get("result", [])
            if not video_list:
                return None

            return [
                {
                    "title": video["title"],
                    "url": video["link"],
                    "duration": video["duration"]
                }
                for video in video_list
            ]
        except Exception as e:
            print(f"[Searcher] Error searching YouTube: {e}")
            return None
