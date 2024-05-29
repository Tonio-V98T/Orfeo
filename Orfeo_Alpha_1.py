# Loading dependencies

# import ffmpeg
import subprocess

import pathlib
import os

import argparse
from argparse import ArgumentParser

### Properly implementing CLI: Windows edition
parser = ArgumentParser(prog = "Orfeo",
                        usage = "Orfeo [url, title, author, path]",
                        description = "Software for downloading and editing music",
                        epilog = "Still in development by Antonio Piscitelli",
                        allow_abbrev = False)

# adding positional arguments to the parser
parser.add_argument("url", help = "Url for fetching the video")#, type = str)
parser.add_argument("title", help = "Choose the song's title")#, type = str)
parser.add_argument("author", help = "Choose the song's author")
parser.add_argument("destination_path", help = "Folder for saving the song")#, type= pathlib.Path)

# print("Parser: ", parser)
print(parser.print_help())

# test instantiating arguments
args = parser.parse_args()

print("\n", args, "\n", args.url, "\n", args.title, "\n",
      args.author, "\n", args.destination_path)

# downloading video
subprocess.run(["yt-dlp",
                "-o",
                f"{args.destination_path}\\{args.author}_{args.title}_Temp_1.webm",
                "-f",
                "251", # opus highest qual
                f"{args.url}"], # song's url
               timeout = 240, check = True)

# removing video
subprocess.run(["ffmpeg",
                "-i",
                f"{args.destination_path}\\{args.author}_{args.title}_Temp_1.webm",
                "-vn", # remove video
                "-c:a", "copy",
                f"{args.destination_path}\\{args.author}_{args.title}_Temp_2.webm"])

# conversion to mka with ffmpeg
subprocess.run(["ffmpeg",
                "-i",
                f"{args.destination_path}\\{args.author}_{args.title}_Temp_2.webm",
                "-c:a", "copy", # already opus codec, else convert with libopus
                f"{args.destination_path}\\{args.author}_{args.title}.mka"], # only audio
               check = True)

# cleaning
os.unlink(f"{args.destination_path}\\{args.author}_{args.title}_Temp_1.webm")
os.unlink(f"{args.destination_path}\\{args.author}_{args.title}_Temp_2.webm")