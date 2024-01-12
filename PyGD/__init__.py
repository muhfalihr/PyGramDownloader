import os

from PyGD.igdownloader import PyGramDownloader
from PyGD.utility import Utility
from PyGD.exception import *
from argparse import ArgumentParser


def main():
    argument_parser = ArgumentParser(
        description="PyGramDownloader is a sophisticated tool designed to facilitate users in downloading images and videos from user posts on the popular social media platform, Instagram."
    )
    argument_parser.add_argument(
        "-func", "--function", type=str, dest="function", help="\"am | allmedia\", \"i | images\""
    )
    argument_parser.add_argument(
        "-p", "--path", type=str, dest="path", help="Path where to save photos or videos.", default=Utility.downloadstorage()
    )
    argument_parser.add_argument(
        "-un", "--username", type=str, dest="username", help="username from profile user account."
    )
    argument_parser.add_argument(
        "-count", "--count", type=int, dest="count", help="The amount of data to be downloaded.", default=33
    )
    argument_parser.add_argument(
        "-max_id", "--max_id", type=str, dest="max_id", help="The key used to load the next page.", default=None
    )
    argument_parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0'
    )
    argument_parser.add_argument(
        "-cookie", "--cookie", type=str, dest="cookie", help="Enter your Instagram browser cookies."
    )

    args = argument_parser.parse_args()

    script_path = os.path.realpath(__file__)
    path = '/'.join(os.path.dirname(script_path).split("/")[:-1])

    if args.cookie:
        Utility.addcookie(args.cookie, path)
    else:
        cookie = Utility.getcookie(path)
        PXD = PyGramDownloader(cookie=cookie)

        match args.function:
            case "allmedia" | "am":
                PXD.allmedia(
                    username=args.username,
                    path=args.path,
                    count=args.count,
                    max_id=args.max_id
                )

            case "images" | "i":
                PXD.images(
                    username=args.username,
                    path=args.path,
                    count=args.count,
                    max_id=args.max_id
                )
            case _:
                raise FunctionNotFoundError(
                    f"Error! The function with the name '{args.function}' is not available."
                )
