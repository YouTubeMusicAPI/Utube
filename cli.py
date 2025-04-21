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
    video_info_list = await searcher.search(query)

    if not video_info_list:
        print("❌ No video found for this query.")
        return

    video_info = video_info_list[0]
    extractor = YouTubeExtractor(video_info['url'])
    video_info = await extractor.extract_info()

    if not video_info:
        print("❌ Failed to extract video info.")
        return

    # Debug: print all available formats
    print("\n📦 Available Formats:")
    for fmt in video_info.get("formats", []):
        print(f"Format: {fmt.get('format')}, Resolution: {fmt.get('resolution')}, Bitrate: {fmt.get('abr')}")

    selector = FormatSelector(video_info)
    selected_format = selector.select_format(quality)

    if not selected_format:
        print(f"❌ No format found for quality: {quality}")
        return

    video_title = video_info.get("title", "untitled").replace(" ", "_").replace("/", "_")
    resolution = selected_format.get("resolution", selected_format.get("abr", "unknown"))
    file_format = selected_format.get("format", "bin")
    output_filename = f"{video_title}_{resolution}.{file_format}"

    downloader = Downloader(selected_format['url'])
    await downloader.download(output_filename)

    if file_format in ["mp4", "webm"]:
        post_processor = PostProcessor(output_filename)
        mp3_path = await post_processor.convert_to_mp3()
        print(f"✅ Video downloaded and converted to MP3: {mp3_path}")
    else:
        print(f"✅ Audio downloaded: {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())
