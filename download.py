import yt_dlp
import os
def get_video_title(url):
    # Options for yt-dlp
    ydl_opts = {
        'quiet': True,  # Suppress output messages
    }

    # Fetch video information using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Set download=False to avoid downloading
        title = info.get('title', None)  # Get the video title from the info dictionary
        return title
    
def get_next_filename(directory, prefix='file_', extension=''):
    # Get a list of all files in the directory with the given prefix
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]

    if not files:
        # If no files found, return the first file name
        return os.path.join(directory, f"{prefix}{1:05d}{extension}")

    # Extract the numeric part of the filenames, and find the highest number
    max_num = max(int(f[len(prefix):].split('.')[0]) for f in files)

    # Create the next file name
    next_num = max_num + 1
    next_filename = f"{prefix}{next_num:05d}{extension}"  # :04d ensures it's zero-padded to 4 digits

    return os.path.join(directory,next_filename)

def save_video_by_url(url, output_path):
    # Options for yt-dlp, specifying the output path
    ydl_opts = {
        'outtmpl': output_path  # Where the file will be saved
    }

    # Download the video using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def save_audio_by_url(url, output_path):
    # Options for yt-dlp to download only audio
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio
        'outtmpl': output_path,      # Path where the file will be saved
        'postprocessors': [{         # Convert to mp3 (or other formats) if needed
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Choose audio format (mp3, m4a, etc.)
            'preferredquality': '192',  # Audio quality (192kbps)
        }],
    }

    # Download the audio using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_video(url, output_dir= './video', save_by_title=False):
    os.makedirs(output_dir, exist_ok=True)
    
    if save_by_title:
        output_path =os.path.join(output_dir, get_video_title(url) + '.mp4')
    else:
        output_path = get_next_filename(output_dir, prefix= 'video_', extension = '.mp4')
    
    save_video_by_url(url, output_path)
    
def download_audio(url, output_dir= './audio', save_by_title=False):
    os.makedirs(output_dir, exist_ok=True)
    
    if save_by_title:
        output_path =os.path.join(output_dir, get_video_title(url) + '.mp3')
    else:
        output_path = get_next_filename(output_dir, prefix= 'audio_', extension = '.mp3')
    
    save_audio_by_url(url, output_path)

my_url = 'https://www.youtube.com/watch?v=Tk9KVJemntA' 
playlist = 'https://www.youtube.com/playlist?list=PLI8FWbwM4CO2ikvIBM3dJTX_RWAQa8WAF'

# Download the audio
download_video(my_url,save_by_title=True)
download_audio(my_url,save_by_title=True)
