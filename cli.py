import sys
import os
import re
import asyncio
from Utube.Extractor import YouTubeExtractor
from Utube.Format_selector import FormatSelector
from Utube.Downloader import Downloader
from Utube.Post_processing import PostProcessor
from Utube.Searcher import YouTubeSearcher

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <video_url_or_search_query> [quality]")
        sys.exit(1)

    query = sys.argv[1]
    quality = sys.argv[2] if len(sys.argv) > 2 else "best"

    searcher = YouTubeSearcher()
    video_info_list = await searcher.search(query)

    if not video_info_list or len(video_info_list) == 0:
        print("Error: No video info found.")
        return

    video_info = video_info_list[0]
    extractor = YouTubeExtractor(video_info['url'])
    video_info = extractor.extract_info()

    if not video_info:
        print("Error: Failed to extract video info.")
        return

    selector = FormatSelector(video_info)
    selected_format = selector.select_format(quality)

    if not selected_format:
        print(f"No available format for quality: {quality}")
        return

    video_title = sanitize_filename(video_info['title'])
    extension = ".mp4" if selected_format['format'] == 'video/mp4' else ".mp3"
    output_filename = f"{video_title}_{selected_format['resolution']}{extension}"

    print(f"[INFO] Selected format URL: {selected_format['url']}")
    print(f"[INFO] Output filename: {output_filename}")

    downloader = Downloader(selected_format['url'])
    await downloader.download(output_filename)

    if not os.path.exists(output_filename):
        print(f"[ERROR] File not found after download: {output_filename}")
        return

    if selected_format['format'] == 'video/mp4':
        post_processor = PostProcessor(output_filename)
        mp3_path = await post_processor.convert_to_mp3()

        if mp3_path and os.path.exists(mp3_path):
            print(f"Video downloaded and converted to MP3: {mp3_path}")
        else:
            print("[ERROR] MP3 conversion failed or file not found.")
    else:
        print(f"Audio downloaded: {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())
