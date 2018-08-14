"""Entry point of application"""

from pytube import YouTube
import os

audio_only = False

print("Welcome user.")

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
        print("Download progress: %dkb remaining" % remaining)

def on_finish_callback(stream, file_handle):
    # Called when download is finished
    print("Download complete.")

def handle_input():
    print("Please input a Youtube video's address. Prepend address with '-a ' to download ony audio.")
    address = input()
    yt = None
    global audio_only
    if address[0:3] == '-a ':
        # Only download audio
        audio_only = True
        yt = YouTube(address[3:])
    else:
        # Download the best progressive stream
        audio_only = False
        yt = YouTube(address)

    print("\nVideo selected.")
    print(yt.title)

    print("\nDownload stream? y/n")
    selection = verify_yn(input())
    print("")

    if selection == 'y':
        # Get a path, verify
        print("Please specify a destination path.")
        path = input()
        while not os.path.isdir(path):
            print("Invalid path, please try again.")
            path = input()

        if audio_only:
            # Download the first audio stream
            print("Downloading audio to Downloads...")
            yt.register_on_progress_callback(progress_callback)
            yt.register_on_complete_callback(on_finish_callback)
            stream = yt.streams.filter(only_audio = True).first().download(path)
        else:
            # Download the first progressive stream to path (max at 720p)
            print("Downloading progressive video to Downloads...")
            yt.register_on_progress_callback(progress_callback)
            yt.register_on_complete_callback(on_finish_callback)
            stream = yt.streams.filter(progressive = True).first().download(path)
    else:
        # Quit the script
        pass

# Start the script
handle_input()
