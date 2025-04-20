import aiohttp
import asyncio
import aiofiles

class Downloader:
    def __init__(self, url):
        self.url = url

    async def download(self, output_path):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status != 200:
                    return
                async with aiofiles.open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
                      
