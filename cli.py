import sys
import asyncio
from Utube.Extractor import YouTubeExtractor
from Utube.Format_selector import FormatSelector
from Utube.Downloader import Downloader
from Utube.Post_processing import PostProcessor
from Utube.Searcher import YouTubeSearcher

async def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <video_url_or_search_query> [quality]")
        sys.exit(1)

    query = sys.argv[1]
    quality = sys.argv[2] if len(sys.argv) > 2 else "best"

    searcher = YouTubeSearcher()
    video = await searcher.search(query)

    if not video:
        print("Error extracting video info.")
        return
        
    video_info = video[0]
    extractor = YouTubeExtractor(video_info['url'])
    video_info = await extractor.extract_info()

    if not video_info:
        print("Error extracting video info.")
        return

    selector = FormatSelector(video_info)
    selected_format = selector.select_format(quality)

    if not selected_format:
        print(f"No available format for quality: {quality}")
        return

    video_title = video_info['title']
    output_filename = f"{video_title}_{selected_format['resolution']}.mp4" if selected_format['format'] == 'video/mp4' else f"{video_title}_{selected_format['resolution']}.mp3"
    
    downloader = Downloader(selected_format['url'])
    await downloader.download(output_filename)

    if selected_format['format'] == 'video/mp4':
        post_processor = PostProcessor(output_filename)
        mp3_path = await post_processor.convert_to_mp3() 
        print(f"Video downloaded and converted to MP3: {mp3_path}")
    else:
        print(f"Audio downloaded: {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())
