import os

from PyGD.igdownloader import PyGramDownloader
from PyGD.utility import Utility
from PyGD.exception import *
from argparse import ArgumentParser


def main():
    """
    PyGramDownloader is a sophisticated tool designed to facilitate users in downloading images and videos from user posts on the popular social media platform, Instagram. With an intuitive interface and powerful functionality, PyGramDownloader allows users to explore and save interesting content from Instagram accounts they admire.

    Key Features of PyGramDownloader:

        - Download Images and Videos:
            PyGramDownloader enables users to download high-quality images and videos from Instagram user posts. With a single click, users can save compelling content to share with friends or keep for later viewing.

        - User-Friendly Interface:
            The PyGramDownloader user interface is designed to provide a seamless and easily understandable user experience. With simple navigation, users can quickly grasp how to use the tool without requiring in-depth technical knowledge.

        - High-Quality Download Options:
            PyGramDownloader provides users with the flexibility to choose the quality of images and videos they want to download. This allows users to save storage space and ensure that the downloaded content aligns with their preferences.

        - Support for Various Instagram Accounts:
            The tool supports downloads from various Instagram accounts, allowing users to explore and download content from friends, celebrities, or other popular accounts.

        - Security and Privacy:
            PyGramDownloader is implemented with a focus on user security and privacy. The tool does not require user login information, ensuring the security of users' Instagram accounts.

        - Regular Updates:
            To maintain availability and reliability, PyGramDownloader receives regular updates. This ensures that the tool can always adapt to the latest changes on the Instagram platform.

    With PyGramDownloader, users can easily explore and collect their favorite content from Instagram, offering a fast, secure, and intuitive downloading experience.

    Created and developed by @muhfalihr.
    """
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
