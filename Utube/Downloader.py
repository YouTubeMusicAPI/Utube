import aiohttp
import aiofiles
import os

class Downloader:
    def __init__(self, download_url):
        self.url = download_url

    async def download(self, filename):
        print(f"[Downloader] Starting download: {self.url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    if resp.status != 200:
                        print(f"[Downloader] Failed to download: HTTP {resp.status}")
                        return

                    async with aiofiles.open(filename, mode='wb') as f:
                        async for chunk in resp.content.iter_chunked(1024 * 1024):
                            await f.write(chunk)

            print(f"[Downloader] Download completed: {filename}")

        except Exception as e:
            print(f"[Downloader] Exception occurred: {str(e)}")
