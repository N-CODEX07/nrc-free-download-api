from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import argparse

def download_youtube_video(url, quality, output_path='.'):
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Get available streams
        video_streams = yt.streams.filter(progressive=False, file_extension='mp4', type='video').order_by('resolution')
        audio_stream = yt.streams.get_audio_only()
        
        # Find closest matching video quality
        selected_video = None
        resolutions = [stream.resolution for stream in video_streams if stream.resolution]
        matching_res = [res for res in resolutions if res == quality]
        
        if matching_res:
            selected_video = next(stream for stream in video_streams if stream.resolution == quality)
        else:
            # Find next lower quality if exact match not available
            for res in reversed(resolutions):
                if int(res[:-1]) <= int(quality[:-1]):
                    selected_video = next(stream for stream in video_streams if stream.resolution == res)
                    print(f"Exact quality not available. Downloading {res} instead.")
                    break
        
        if not selected_video:
            raise Exception(f"No stream available at or below {quality} resolution")
        
        # Sanitize filename
        title = ''.join(c for c in yt.title if c.isalnum() or c in ' -_')
        video_file = f"temp_video_{title}.mp4"
        audio_file = f"temp_audio_{title}.mp4"
        output_file = os.path.join(output_path, f"{title}.mp4")
        
        # Download streams
        print("Downloading video stream...")
        selected_video.download(filename=video_file)
        print("Downloading audio stream...")
        audio_stream.download(filename=audio_file)
        
        # Merge video and audio
        print("Merging streams...")
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # Clean up temp files
        os.remove(video_file)
        os.remove(audio_file)
        
        print(f"\nSuccessfully downloaded: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Video Downloader')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('quality', help='Video quality (e.g., 720p, 1080p)')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    download_youtube_video(args.url, args.quality, args.output)
