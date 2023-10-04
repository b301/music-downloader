#!/usr/bin/python3

import os
import glob
import sys

# make sure to install this
import yt_dlp


DEBUG = False
FORMAT = 'm4a'


def remove_gib(fname: str) -> str:
    fob = fname.rfind('[')
    fcb = fname.rfind('.')

    if fob == -1:
        debug(f'error: {fname} resulted in fob = -1')
        return fname
    
    fnew = fname.replace(fname[fob:fcb], '')
    os.rename(fname, fnew)

    return fnew

def remove_trailing_spaces(fname: str):
    fparts = fname.rsplit('.', 1)
    fnew = f'{fparts[0].rstrip()}.{fparts[1]}'

    os.rename(fname, f'{fparts[0].rstrip()}.{fparts[1]}')

    return fnew

def remove_gibberish(fformat: str):
    files = glob.glob(f'{os.getcwd()}/*.{fformat}')
    for f in files:
        debug(f)
        f = remove_gib(f)
        debug(f'post remove_gib {f}')
        f = remove_trailing_spaces(f)
        debug(f'post remove_trailing_spaces {f}')

    debug('removed all gibberish')


def debug(*args):
    if DEBUG:
        print(*args)


def download_from_url(ydl: yt_dlp.YoutubeDL, url: str):
    ydl.download([url])


def main():
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors':
        [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': FORMAT
            },
            {
                'key': 'EmbedThumbnail',
            },

        ],
        'writethumbnail': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        args = sys.argv[1:]

        if len(args) > 1:
            print("Too many arguments.")
            print("Usage: python uberdownloader.py")
            exit()
        elif len(args) == 0:
            url=input("Enter Youtube URL (playlist or a single video): ")
            download_from_url(ydl, url)

    remove_gibberish(FORMAT)


if __name__ == "__main__":
    main()