from pytube import Playlist, YouTube
from moviepy.editor import *
import clipboard


def download_youtube_video(url, convert_to_mp3=True):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(output_path=dest_folder)

    # get the video file
    video_file = os.path.join(dest_folder, video.default_filename)

    if convert_to_mp3:
        convert_video_to_mp3(video_file)

def convert_video_to_mp3(video_file):
    # get the video file
    video = VideoFileClip(video_file)

    # convert the video to mp3
    video.audio.write_audiofile(video_file.replace('.mp4', '') + '.mp3')

    # close the video file
    video.close()

    # remove the original video file
    os.remove(video_file)

def download_and_convert_playlist(url, dest_folder, convert_to_mp3=True):
    pl = Playlist(url)

    for video_url in pl.video_urls:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path=dest_folder)

        # get the video file
        video_file = os.path.join(dest_folder, video.default_filename)

        # convert the video to mp3
        if convert_to_mp3:
            convert_video_to_mp3(video_file)

# ...

# Get the playlist link from the user
playlist_link = clipboard.paste()
print("Link from clipboard is used: " + playlist_link)

while playlist_link == '' or playlist_link == None or playlist_link.find('https://', 0, len('https://')) == -1 and playlist_link.find('http://', 0, len('http://')) == -1:
    playlist_link = input("Please Enter a valid link: ")

# Get the destination folder from the user
dest_folder = input("Enter the destination folder: ")

# check if the user wants to convert to mp3
convert_to_mp3 = input("Convert to mp3? (y/n): ")
while convert_to_mp3.lower() not in ['y', 'n']:
    convert_to_mp3 = input("Convert to mp3? (y/n): ")

if convert_to_mp3.lower() == 'y':
    convert_to_mp3 = True
else:
    convert_to_mp3 = False

# Check if the user entered a valid playlist link and destination folder
if dest_folder == '': 
    print("Please enter a valid playlist link and destination folder.")
    exit()

# Check if the destination folder exists
if not os.path.exists(dest_folder):
    print("Destination folder does not exist. Creating it...")
    os.makedirs(dest_folder)

if not playlist_link.find('list=') == -1:
    download_and_convert_playlist(playlist_link, dest_folder, convert_to_mp3)
else:
    download_youtube_video(playlist_link, convert_to_mp3)
    
print("Done! Enjoy your music.")