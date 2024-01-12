import re
import json
import requests

from requests.sessions import Session
from urllib.parse import urljoin, unquote, quote
from datetime import datetime
from PyGD.utility import Utility
from PyGD.exception import *
from faker import Faker
from typing import Any, Optional
from tqdm import tqdm


class PyGramDownloader:
    def __init__(self, cookie: str) -> Any:
        if not isinstance(cookie, str):
            raise TypeError("Invalid parameter for 'PyGramDownloader'. Expected str, got {}".format(
                type(cookie).__name__)
            )
        self.__cookie = cookie
        self.__session = Session()
        self.__fake = Faker()

        self.__headers = dict()
        self.__headers["Accept"] = "application/json, text/plain, */*"
        self.__headers["Accept-Language"] = "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        self.__headers["Sec-Fetch-Dest"] = "empty"
        self.__headers["Sec-Fetch-Mode"] = "cors"
        self.__headers["Sec-Fetch-Site"] = "same-site"
        self.__headers["Cookie"] = cookie

    def __Csrftoken(self) -> str:
        pattern = re.compile(r'csrftoken=([a-zA-Z0-9_-]+)')
        matches = pattern.search(self.__cookie)
        if matches:
            csrftoken = matches.group(1)
            return csrftoken
        else:
            raise CSRFTokenMissingError(
                "Error! CSRF token is missing. Please ensure that a valid CSRF token is included in the cookie."
            )

    def __processmedia(self, item: dict, func_name: str) -> list:
        if not isinstance(item, dict):
            raise TypeError("Invalid parameter for '__processmedia'. Expected dict, got {}".format(
                type(item).__name__)
            )
        if not isinstance(func_name, str):
            raise TypeError("Invalid parameter for '__processmedia'. Expected str, got {}".format(
                type(func_name).__name__)
            )

        medias = []

        match func_name:
            case "allmedia":
                images = [
                    index["image_versions2"]["candidates"][0]["url"]
                    for index in item.get(
                        "carousel_media", [item]
                    )
                ]

                videos = [
                    media["video_versions"][0]["url"]
                    for media in item.get(
                        "carousel_media", [item]
                    ) if "video_versions" in media
                ]
                medias.extend(images + videos)

            case "images":
                images = [
                    index["image_versions2"]["candidates"][0]["url"]
                    for index in item.get(
                        "carousel_media", [item]
                    )
                ]
                medias.extend(images)
        return medias

    def __download(self, url: str) -> Any:
        if not isinstance(url, str):
            raise TypeError("Invalid parameter for '__download'. Expected str, got {}".format(
                type(url).__name__)
            )

        user_agent = self.__fake.user_agent()
        self.__headers["User-Agent"] = user_agent
        resp = self.__session.request(
            "GET",
            url=url,
            timeout=60,
            headers=self.__headers,
        )
        status_code = resp.status_code
        data = resp.content
        if status_code == 200:
            pattern = re.compile(r'\/([^\/?]+\.jpg)')
            matches = pattern.search(url)
            if matches:
                filename = matches.group(1)
            else:
                pattern = re.compile(r'\/([^\/?]+\.mp4)')
                matches = pattern.search(url)
                if matches:
                    filename = matches.group(1)
                else:
                    raise URLValidationError(
                        f"Error! Invalid URL \"{url}\". Make sure the URL is correctly formatted and complete."
                    )
            return data, filename
        else:
            raise HTTPErrorException(
                f"Error! status code {resp.status_code} : {resp.reason}"
            )

    def allmedia(
            self,
            username: str,
            path: str,
            count: Optional[int | str] = 33,
            max_id: Optional[str] = None,
            proxy: Optional[str] = None,
            **kwargs
    ) -> Any:

        if not isinstance(username, str):
            raise TypeError("Invalid parameter for 'allmedia'. Expected str, got {}".format(
                type(username).__name__)
            )
        if not isinstance(path, str):
            raise TypeError("Invalid parameter for 'allmedia'. Expected str, got {}".format(
                type(path).__name__)
            )
        if not isinstance(count, (int | str)):
            raise TypeError("Invalid parameter for 'allmedia'. Expected int|str, got {}".format(
                type(count).__name__)
            )
        if max_id is not None:
            if not isinstance(max_id, str):
                raise TypeError("Invalid parameter for 'allmedia'. Expected str, got {}".format(
                    type(max_id).__name__)
                )
        if proxy is not None:
            if not isinstance(proxy, str):
                raise TypeError("Invalid parameter for 'allmedia'. Expected str, got {}".format(
                    type(proxy).__name__)
                )

        Utility.mkdir(path=path)

        print(
            f"Downloading all image from Instagram users with the name @{username}."
        )
        print(f"Saved in path: \"{path}\"")

        user_agent = self.__fake.user_agent()
        url = f"https://www.instagram.com/api/v1/feed/user/{username}/username/?count={count}"\
            if max_id else f"https://www.instagram.com/api/v1/feed/user/{username}/username/?count={count}&max_id={max_id}"
        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Asbd-Id"] = "129477"
        self.__headers["X-Csrftoken"] = self.__Csrftoken()
        self.__headers["X-Ig-App-Id"] = "936619743392459"
        resp = self.__session.request(
            method="GET",
            url=url,
            headers=self.__headers,
            timeout=60,
            proxies=proxy,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            next_max_id = data.get("next_max_id", "")

            medias = []
            for item in data["items"]:
                medias_result = self.__processmedia(
                    item=item,
                    func_name=Utility.current_funcname()
                )
                medias.extend(medias_result)

            for link in tqdm(medias, desc="Downloading"):
                try:
                    data_content, filename = self.__download(url=link)
                    with open(f"{path}/{filename}", "wb") as file:
                        file.write(data_content)
                except RequestProcessingError:
                    raise RequestProcessingError(
                        "FAILED! Error processing the request!"
                    )
            print("DONE!!!🥳🥳🥳")
            print(f"next_max_id for next page \"{next_max_id}\"")
        else:
            raise HTTPErrorException(
                f"Error! status code {resp.status_code} : {resp.reason}"
            )

    def images(
            self,
            username: str,
            path: str,
            count: Optional[int | str] = 33,
            max_id: Optional[str] = None,
            proxy: Optional[str] = None,
            **kwargs
    ) -> Any:

        if not isinstance(username, str):
            raise TypeError("Invalid parameter for 'images'. Expected str, got {}".format(
                type(username).__name__)
            )
        if not isinstance(path, str):
            raise TypeError("Invalid parameter for 'images'. Expected str, got {}".format(
                type(path).__name__)
            )
        if not isinstance(count, (int | str)):
            raise TypeError("Invalid parameter for 'images'. Expected int|str, got {}".format(
                type(count).__name__)
            )
        if max_id is not None:
            if not isinstance(max_id, str):
                raise TypeError("Invalid parameter for 'images'. Expected str, got {}".format(
                    type(max_id).__name__)
                )
        if proxy is not None:
            if not isinstance(proxy, str):
                raise TypeError("Invalid parameter for 'images'. Expected str, got {}".format(
                    type(proxy).__name__)
                )

        Utility.mkdir(path=path)

        print(
            f"Downloading all image from Instagram users with the name @{username}."
        )
        print(f"Saved in path: \"{path}\"")

        user_agent = self.__fake.user_agent()
        url = f"https://www.instagram.com/api/v1/feed/user/{username}/username/?count={count}"\
            if max_id else f"https://www.instagram.com/api/v1/feed/user/{username}/username/?count={count}&max_id={max_id}"
        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Asbd-Id"] = "129477"
        self.__headers["X-Csrftoken"] = self.__Csrftoken()
        self.__headers["X-Ig-App-Id"] = "936619743392459"
        resp = self.__session.request(
            method="GET",
            url=url,
            headers=self.__headers,
            timeout=60,
            proxies=proxy,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            next_max_id = data.get("next_max_id", "")

            medias = []
            for item in data["items"]:
                medias_result = self.__processmedia(
                    item=item,
                    func_name=Utility.current_funcname()
                )
                medias.extend(medias_result)

            for link in tqdm(medias, desc="Downloading"):
                try:
                    data_content, filename = self.__download(url=link)
                    with open(f"{path}/{filename}", "wb") as file:
                        file.write(data_content)
                except RequestProcessingError:
                    raise RequestProcessingError(
                        "FAILED! Error processing the request!"
                    )
            print("DONE!!!🥳🥳🥳")
            print(f"next_max_id for next page \"{next_max_id}\"")
        else:
            raise HTTPErrorException(
                f"Error! status code {resp.status_code} : {resp.reason}"
            )


if __name__ == "__main__":
    cookie = 'mid=ZZvoXwAEAAGlwVYJ5LW1bmn7R-EP; ig_did=AFD90341-FBE2-4EC2-9AD4-119ED91489F6; ig_nrcb=1; datr=XuibZa27KKTrPW9KB1hfJ9BB; ds_user_id=63948446931; dpr=0.8999999761581421; csrftoken=drx5GLrM3ig5q6RLgVKCNjYPTicOeprb; sessionid=63948446931%3ApdsBTPZe3hW2uf%3A10%3AAYfkN2z2nh9Jkn7enJ9gX6-t9VFE3KBrlvU0LMohTA; rur="NHA\05463948446931\0541736316293:01f7f869bfd8bba8c027aeccbe66712c6a825083d92893ca4f4a5a9a3e3912d022c129ee"'
    sb = PyGramDownloader(cookie=cookie)