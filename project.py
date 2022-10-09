import os
import re
from PIL import Image
from simple_term_menu import TerminalMenu
from pytube import YouTube
from pytube import Playlist
from pathlib import Path

class StreamsId:
    def __init__(self):
        self.m_items = []
        self.m_id = {}
    def check(self):
        if not len(self.m_id) == len(self.m_items):
            raise ValueError("The length does not match")
        return 0
    def clear(self):
        self.m_items = []
        self.m_id = {}

default = {'title':'S-Utils\n',  'menu_cursor':'', 'cycle_cursor':True, 'clear_screen':True}

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    opts = ['Youtube Downloader', 'Image Converter', 'Exit']
    menu = TerminalMenu(opts, **default)
    opt = menu.show()

    if opts[opt] == 'Exit':
        os.system('cls' if os.name == 'nt' else 'clear')
        return 0
    elif opts[opt] == 'Youtube Downloader':
        ytd()
    elif opts[opt] == 'Image Converter':
        ic()


def ytd():
    os.system('cls' if os.name == 'nt' else 'clear')
    container = StreamsId()
    opts = ['Download Video', 'Download Playlist', 'Back']
    menu = TerminalMenu(opts, **default)
    opt = menu.show()
    if opts[opt] == 'Back':
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    elif opts[opt] == 'Download Video':
        youtube_downloader(container)
    elif opts[opt] == 'Download Playlist':
        youtube_playlist_downloader(container)

def youtube_downloader(container):
    while True:
        try:
            yt = YouTube(input('Video Url: '), on_progress_callback=progress, on_complete_callback=complete)
            break
        except:
            continue

    for item in yt.streams.order_by('type'):

        m = re.search(r"itag=\"(?P<id>[0-9]*)\" mime_type=\"(?P<mtp>.*)\" (?P<qlt>res=\"([0-9]*p)\"|abr=\"([0-9]*kbps)\") (?P<etc>.*) type=\"(?P<tp>.*)\"", str(item))

        id = int(m.group('id'))
        tp = m.group('tp')
        ql = m.group('qlt')
        mtp = m.group('mtp')
        et = str(m.group('etc'))

        container.m_items.append(f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}")
        container.m_id[f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}"] = id

    container.check()
    os.system('cls' if os.name == 'nt' else 'clear')
    options = list(container.m_items)

    terminal_menu = TerminalMenu(options, **default)
    menu_entry_index = terminal_menu.show()

    # uses the menu entry value in the dictionary
    stream = yt.streams.get_by_itag(container.m_id[str(options[menu_entry_index])])
    stream.download('download')

    container.clear()

    ytd()

def youtube_playlist_downloader(container):
    while True:
        try:
            ytp = Playlist(input('Playlist URL: '))
            break
        except:
            continue

    for item in ytp.videos[0].streams.order_by('type'):

        m = re.search(r"itag=\"(?P<id>[0-9]*)\" mime_type=\"(?P<mtp>.*)\" (?P<qlt>res=\"([0-9]*p)\"|abr=\"([0-9]*kbps)\") (?P<etc>.*) type=\"(?P<tp>.*)\"", str(item))

        id = int(m.group('id'))
        tp = m.group('tp')
        ql = m.group('qlt')
        mtp = m.group('mtp')
        et = str(m.group('etc'))

        container.m_items.append(f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}")
        container.m_id[f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}"] = id

    container.check()
    os.system('cls' if os.name == 'nt' else 'clear')
    options = list(container.m_items)

    terminal_menu = TerminalMenu(options, **default)
    menu_entry_index = terminal_menu.show()

    # uses the menu entry value in the dictionary
    for i, video in enumerate(ytp.videos):
        try:
            stream = video.streams.get_by_itag(container.m_id[str(options[menu_entry_index])])
            stream.download('download/playlist')
            print(f'Downloading: {ytp.videos[i].title}')
        except:
            print(f'Couldn\'t Download {ytp.videos[i].title} video with selected settings, using default')
            stream = video.streams.get_highest_resolution()
            stream.download('download/playlist')
            print(f'Downloading: {ytp.videos[i].title}')

    container.clear()
    ytd()


def progress(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = int(((size - bytes_remaining) / size) * 100)
    print(progress)
    os.system('cls' if os.name == 'nt' else 'clear')
    # do call progress bar from GUI here

def complete(stream, file_handle):
    print('Download Finished')
# --------------------------------#
def ic():
    os.system('cls' if os.name == 'nt' else 'clear')
    opts = list_files()
    menu = TerminalMenu(opts, **default, multi_select=True, show_multi_select_hint=True,)
    _ = menu.show()
    selected = menu.chosen_menu_entries
    if selected:
        convert(list(selected))
        main()

def list_files(directory="./images"):
    return (file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)))

def convert(files):
    opt = ["bmp", "png", "jpeg", "DIB", "DDS", "ICO", "WebP"]
    terminal_menu = TerminalMenu(opt, **default)
    idx = terminal_menu.show()

    for it in files:
        name, sep, ext = it.rpartition('.')

        base = Path.cwd() / 'images' / it
        out = Path.cwd() / 'images' / 'output' / f'{name}.{opt[idx]}'

        im = Image.open(base)
        rgb_im = im.convert("RGBA")
        rgb_im.save(out)

        im.close()
        rgb_im.close()

    return 0

if __name__ == "__main__":
    main()