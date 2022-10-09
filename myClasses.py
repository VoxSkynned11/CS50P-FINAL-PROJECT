import sys
import os
import re
import pytube
from PIL import Image
from simple_term_menu import TerminalMenu
from pytube import YouTube
from pytube import Playlist
from pathlib import Path



default = {'title':'S-Utils\n',  'menu_cursor':'', 'cycle_cursor':True, 'clear_screen':True}


class StreamsId:
    def __init__(self):
        self.m_items = []
        self.m_id = {}

    def check(self):
        if not len(self.m_id) == len(self.m_items):
            raise ValueError("The length does not match")

class Ytd(TerminalMenu):
    def __init__(self):
        self.opts = ['Download Video', 'Download Playlist', 'Back']
        super().__init__(self.opts, **default)
        self.container = StreamsId()

    def run(self):
        self.idx = self.show()
        self.choice = self.opts[self.idx]
        if self.choice == 'Back':
            os.system('cls' if os.name == 'nt' else 'clear')
            main = Main()
            main.run()
        elif self.choice == 'Download Video':
            self.youtube_downloader()
        elif self.choice == 'Download Playlist':
            self.youtube_playlist_downloader()

    def youtube_downloader(self):
        while True:
            try:
                self.yt = YouTube(input('Video Url: '), on_progress_callback=self.progress_function, on_complete_callback=self.complete)
                break
            except:
                continue

        for item in self.yt.streams.order_by('type'):

            m = re.search(r"itag=\"(?P<id>[0-9]*)\" mime_type=\"(?P<mtp>.*)\" (?P<qlt>res=\"([0-9]*p)\"|abr=\"([0-9]*kbps)\") (?P<etc>.*) type=\"(?P<tp>.*)\"", str(item))

            id = int(m.group('id'))
            tp = m.group('tp')
            ql = m.group('qlt')
            mtp = m.group('mtp')
            et = str(m.group('etc'))

            self.container.m_items.append(f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}")
            self.container.m_id[f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}"] = id

        self.container.check()
        os.system('cls' if os.name == 'nt' else 'clear')
        options = list(self.container.m_items)

        terminal_menu = TerminalMenu(options, **default)
        menu_entry_index = terminal_menu.show()

        # uses the menu entry value in the dictionary
        self.stream = self.yt.streams.get_by_itag(self.container.m_id[str(options[menu_entry_index])])
        self.stream.download('download')

        self.clean()

        self.run()


    def youtube_playlist_downloader(self):
        while True:
            try:
                self.ytp = Playlist(input('Playlist URL: '))
                break
            except:
                continue

        for item in self.ytp.videos[0].streams.order_by('type'):

            m = re.search(r"itag=\"(?P<id>[0-9]*)\" mime_type=\"(?P<mtp>.*)\" (?P<qlt>res=\"([0-9]*p)\"|abr=\"([0-9]*kbps)\") (?P<etc>.*) type=\"(?P<tp>.*)\"", str(item))

            id = int(m.group('id'))
            tp = m.group('tp')
            ql = m.group('qlt')
            mtp = m.group('mtp')
            et = str(m.group('etc'))

            self.container.m_items.append(f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}")
            self.container.m_id[f"Type: {mtp} Quality: {ql} ### Additional Info: {tp}-{et}"] = id

        self.container.check()
        os.system('cls' if os.name == 'nt' else 'clear')
        options = list(self.container.m_items)

        terminal_menu = TerminalMenu(options, **default)
        menu_entry_index = terminal_menu.show()

        # uses the menu entry value in the dictionary
        for i, video in enumerate(self.ytp.videos):
            try:
                self.stream = video.streams.get_by_itag(self.container.m_id[str(options[menu_entry_index])])
                self.stream.download('download/playlist')
                print(f'Downloading: {self.ytp.videos[i].title}')
            except:
                print(f'Couldn\'t Download {self.ytp.videos[i].title} video with selected settings, using default')
                self.stream = video.streams.get_highest_resolution()
                self.stream.download('download/playlist')
                print(f'Downloading: {self.ytp.videos[i].title}')

        self.clean()
        self.run()


    """https://stackoverflow.com/questions/49185538/how-to-add-progress-bar"""
    pytube.request.default_range_size = 1048576    # this is for chunck size, 1MB size

    def progress_function(self, stream, chunk, bytes_remaining):
        size = self.stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        print(progress)
        os.system('cls' if os.name == 'nt' else 'clear')
        # do call progress bar from GUI here

    """https://stackoverflow.com/questions/49185538/how-to-add-progress-bar"""
    def complete(self, stream, file_handle):
        print("Download Finished")
        # progress bar stop call from GUI here


    def clean(self):
        self.container.m_items = []
        self.container.m_id = {}


class Ic(TerminalMenu):
    def __init__(self):
        self.opts = self.list_files()
        super().__init__(self.opts, **default, multi_select=True,
        show_multi_select_hint=True,)

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.idx = self.show()
        self.selected = self.chosen_menu_entries
        if self.selected:
            self.convert(list(self.selected))
        s = input("Continue? Y/N ").lower()
        if not s in ['y','yes']:
            os.system('cls' if os.name == 'nt' else 'clear')
            m = Main()
            m.run()
        else:
            self.run()

    def convert(self, its):
        opt = ["bmp", "png", "jpeg", "DIB", "DDS", "ICO", "WebP"]
        terminal_menu = TerminalMenu(opt, **default)
        idx = terminal_menu.show()


        for it in its:
            name, sep, ext = it.rpartition('.')

            base = Path.cwd() / 'images' / it
            out = Path.cwd() / 'images' / 'output' / f'{name}.{opt[idx]}'

            im = Image.open(base)
            rgb_im = im.convert("RGBA")
            rgb_im.save(out)

            im.close()
            rgb_im.close()


    def list_files(self, directory="./images"):
        return (file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)))


class Main(TerminalMenu):
    def __init__(self):
        self.opts = ['Youtube Downloader', 'Image Converter', 'Exit']
        super().__init__(self.opts, **default)

    def run(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        self.idx = self.show()
        self.choice = self.opts[self.idx]

        if self.choice == 'Exit':
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit('Exited')
        elif self.choice == 'Youtube Downloader':
            ytd = Ytd()
            ytd.run()
        elif self.choice == 'Image Converter':
            ic = Ic()
            ic.run()


