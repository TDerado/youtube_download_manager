import argparse
from pytubefix import YouTube
#from pytubefix.cli import on_progress
from pytube.exceptions import VideoUnavailable, AgeRestrictedError, VideoPrivate, MembersOnly, VideoRegionBlocked, MaxRetriesExceeded
from tqdm import tqdm
import os
import re

class ProgressBar(tqdm):
    def update_to(self, stream, chunk, bytes_remaining):
        """displays the precentage of download completion"""
        total = stream.filesize
        downloaded = total - bytes_remaining
        #download_percentage = downloaded / total * 100
        self.total = total
        self.update(downloaded - self.n)
        self.refresh()
        #print(f"Downloading: {download_percentage:.2f}%")

def build_arg():
    '''creates the argument parser and recieves the arguments given'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help = "YouTube link for installation", required=True)
    parser.add_argument("-r", "--resolution", help = "desired resolution for downloaded video, can use 'h' and 'l' for highest and lowest resolutions")
    parser.add_argument("-o", "--output", help = "Directory to store downloaded video")
    try:
        args = parser.parse_args()
        return args
    except Exception as e:
        print(f'unknown error has occured: {e}')
        return None
    
def download_link(url, resolution="h", output="my_downloads"):
    '''url = youtube link (str) | resolution = "1080p" (str) | output = directory (str)
        takes the given url and tries to find a video with the given resolution, and innstalls it into the given directory
    '''
    t = ProgressBar(unit='B', miniters=1)
    yt = YouTube(url, on_progress_callback=t.update_to)
    if re.search('[^A-Za-z0-9 _]+', output):
        output = re.sub('[^A-Za-z0-9 _]+', '', output)
        print(f"\nOutput file cannot have special characters, modifiying output folder name >>> {output}")
    try:
        folder_name = re.sub('[^A-Za-z0-9 _]+', '', yt.title)
        if resolution == 'h':
            stream = yt.streams.filter(only_video=True, progressive=False).first()
        elif resolution == 'l':
            stream = yt.streams.filter(only_video=True, progressive=False).last()
        else:
            stream = yt.streams.filter(res=resolution, only_video=True, progressive=False).first()
    except Exception as e:
        print(f"Video URL is not available: {e}")
        return -2
    
    if stream is not None:
        try:
            folder_name = re.sub('[^A-Za-z0-9 ]+', '', yt.title)
            print(f'\nDownloading video: {url}')
            with t:
                stream.download(output_path=f"{output}\\{folder_name}")
                audio = yt.streams.filter(only_audio=True)
                print(f'\nDownloading audio: {url}')
                audio[0].download(output_path=f"{output}\\{folder_name}")
        except AgeRestrictedError:
            print('Cannot download a age restricted video!')
            return -2
        except (VideoRegionBlocked, VideoPrivate, MembersOnly) as e:
            print(f'Cannot download video! Access was denied: {e}')
            return -2
        except VideoUnavailable:
            print('Cannot download video! The video was unavailable')
            return -2
        except Exception as e:
            print(f'Was not able to install video due to unseen error: {e}')
            return -2
    else:
        return -1
    return 1

if __name__ == "__main__":
    args = build_arg()
    url = ""
    resolution = "h"
    output = "my_downloads"

    if args is None:
        print('could not process the arguments cancelling...')
        raise SystemExit
    try:
        url = args.url
        if args.resolution is not None:
            resolution = args.resolution
        if args.output is not None:
            output = args.output
        if "https://www.youtube.com/" not in url:
            print('URL does not appear to be a youtube link, cancelling...')
            raise SystemExit
    except Exception as e:
        print(f'unknown error with argument construction: {e}, cancelling...')
        raise SystemExit from e
    
    result = download_link(url, resolution=resolution, output=output)
    if result == -1:
        print(f"No videos of resolution {resolution} found")
        choice = "temp"
        while choice.lower().strip() != 'h' or choice.lower().strip() == 'l':
            choice = input("Install highest or lowest resolution found? (h/l): ")
            if choice.lower().strip() == 'h':
                result = download_link(url, resolution='h', output=output)
                break
            if choice.lower().strip() == 'l':
                result = download_link(url, resolution='l', output=output)
                break