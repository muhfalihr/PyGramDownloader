import unicodedata
import hashlib
import json
import pytz
import re
import os

from datetime import datetime
from PyGD.exception import *
from typing import Any


class Utility:
    """
    Encapsulates a collection of utility functions for various tasks.
    """
    @staticmethod
    def hashmd5(url: str) -> str:
        """Calculates the MD5 hash of the given URL.
        Returns the hashed value as a hexadecimal string.
        """
        md5hash = hashlib.md5()
        md5hash.update(url.encode('utf-8'))
        hashed = md5hash.hexdigest()
        return hashed

    @staticmethod
    def timezone(date_time: str, format: str) -> str:
        """Converts a datetime string to the corresponding time zone offset for Asia/Jakarta.
        Takes the datetime string, a format string specifying its format, and returns the offset as a string like "+0700".
        """
        tz = pytz.timezone("Asia/Jakarta")
        date = datetime.strptime(date_time, format)
        timezone = tz.localize(date).strftime("%z")
        return timezone

    @staticmethod
    def UniqClear(text: str) -> str:
        """Normalizes and removes non-ASCII characters from the given text.
        Returns the ASCII-only version of the text.
        """
        normalized = unicodedata.normalize('NFKD', text)
        ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
        return ascii_text

    @staticmethod
    def makeunique(datas: list) -> list:
        """
        Removes duplicate elements from a list while preserving order.
        Returns a new list containing only unique elements.
        """
        unique_list = []
        [unique_list.append(x) for x in datas if x not in unique_list]
        return unique_list

    @staticmethod
    def convertws(data: dict) -> str:
        """
        Converts dict data to string and removes spaces at the end of the text.
        """
        dumps = json.dumps(data)
        without_whitespace = re.sub(r'\s+', '', dumps)
        return without_whitespace

    @staticmethod
    def current_funcname() -> str:
        """
        Calls the name of the function used.
        """
        import inspect
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame)[1]
        function_name = caller_frame[3]
        return function_name

    @staticmethod
    def mkdir(path: str) -> Any:
        """
        Check whether the given path exists in the system, if not, a new folder will be created with a name that matches the given path.
        """
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print("Created a new folder because the given folder does not exist.")
            except OSError as e:
                raise e

    @staticmethod
    def downloadstorage():
        """
        Used to determine the default storage location for downloaded results.
        """
        if os.name == 'posix':  # Linux/Mac
            location = os.path.join(os.path.expanduser('~'), 'Downloads')
            return location
        elif os.name == 'nt':  # Windows
            location = os.path.join(os.path.expanduser('~'), 'Downloads')
            return location
        else:
            return None  # Other Operation System

    @staticmethod
    def addcookie(cookie: str, path: str) -> Any:
        """
        Create a cookie file to store cookies from user input.
        """
        try:
            with open(f"{path}/cookie", "w") as cookie_file:
                cookie_file.write(cookie)
            print(
                f"SUCCES: The cookie file has been created and saved in the path \"{path}\"."
            )
        except CookieCreationError:
            raise CookieCreationError(
                f"FAILED: An error occurred while trying to create a cookie file"
            )

    @staticmethod
    def getcookie(path: str) -> str:
        """
        Retrieves cookies from the cookie file in the form of a string.
        """
        try:
            with open(f"{path}/cookie", "r") as cookie_file:
                cookie = cookie_file.read()
            return cookie
        except FileNotFoundError:
            raise CookieFileNotFoundError(
                "Error: Cookie file not found. Please check if the cookie file exists."
            )
