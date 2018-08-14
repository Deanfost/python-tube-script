"""Entry point of application"""

from pytube import YouTube
from ffmpy import FFmpeg
import os

audio_only = False
print("\nWelcome user.")

def verify_yn(selection):
    # Only accept 'y/n'
    if not(selection == 'n' or selection == 'y'):
        print("Invalid selection.\n")
        return verify_yn(input())
    return selection

def progress_callback(stream, chunk, file_handle, bytes_remaining):
    # Called everytime there is a progress update
    remaining = int(bytes_remaining * .0001)
    # Limit the print rate
    if remaining % 5 == 0:
        print("Download progress: %dKB remaining" % remaining)

def on_finish_callback(stream, file_handle):
    # Called when download is finished
    size = int(stream.filesize * .00001)
    print("Download complete (%sMB)." % size)

def handle_input():
    print("Usage: '[Video address] [Destination path]'")

    console = input()

    # Parse the command, check syntax
    params = console.split(' ')
    if len(params) != 2:
        print("Invalid syntax.")
        return

    address = params[0]
    path = params[1]

    # Verify path
    if not os.path.isdir(path):
        print("Invalid path.")
        return

    yt = YouTube(address)

    print("\nVideo selected.")
    print(yt.title + "\n(Best progressive stream)")
    print("To path: " + path)

    print("\nDownload stream? y/n")
    selection = verify_yn(input())
    print("")

    if selection == 'y':
        print("Downloading progressive video to path...")
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(on_finish_callback)
        stream = yt.streams.filter(progressive = True).first().download(path)
    else:
        # Quit the script
        return

# Start the script
handle_input()
