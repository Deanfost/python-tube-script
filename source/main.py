"""Entry point of application"""

import pytube

import os
import sys
import math

path = ""

print("\nWelcome user.")

def verify_yn(selection):
    # Only accept 'y/n'
    if not(selection == 'n' or selection == 'y'):
        print("Invalid selection.\n")
        return verify_yn(input())
    return selection

def progress_callback(stream, chunk, file_handle, bytes_remaining):
    # Called everytime there is a progress update
    remaining = math.ceil(bytes_remaining * .0001)
    # Limit the print rate
    if remaining % 5 == 0:
        sys.stdout.write("Download progress: %dKB \r" % remaining)

def on_finish_callback(stream, file_handle):
    # Called when download is finished
    size = math.ceil(stream.filesize * .000001)
    print("Download complete (%sMB)." % size)

def handle_input():
    print("Usage: '[Video address] [(optional) Destination path]'")

    console = input()

    # Parse the command, check syntax
    params = console.split(' ')
    if len(params) > 2 or len(params) == 0:
        print("Invalid syntax.")
        return

    global path
    address = params[0]

    if len(params) == 2:
        path = params[1]

    # Verify path if specified
    if path != "" and not os.path.isdir(path):
        print("Invalid path.")
        return

    try:
        print("Fetching video...");
        yt = pytube.YouTube(address)

        print("\nVideo selected.")
        print(yt.title + "\n(Best progressive stream)")
        if path != "":
            print("To path: " + path)
        else:
            print("To working directory.")

        print("\nDownload stream? y/n")
        selection = verify_yn(input())
        print("")

        if selection == 'y':
            print("Downloading progressive video to path...")
            yt.register_on_progress_callback(progress_callback)
            yt.register_on_complete_callback(on_finish_callback)
            if path != "":
                stream = yt.streams.filter(progressive = True).first().download(path)
            else:
                stream = yt.streams.filter(progressive = True).first().download()
        else:
            # Quit the script
            return
    except pytube.exceptions.RegexMatchError:
        print("Invalid video address.")

# Start the script
if __name__ == "__main__":
    handle_input()
else:
    print("Please run 'main.py' as the top-level script.")
