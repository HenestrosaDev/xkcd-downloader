import re
import time
from pathlib import Path
from tkinter import filedialog

import bs4
import constants as c
import httpx
import models


def main():
    xkcd_directory = get_xkcd_directory()
    latest_xkcd_in_dir = get_latest_xkcd_in_dir(
        xkcd_directory / c.XKCD_SUBDIRECTORY_NAMES[0]
    )

    if (latest_xkcd_in_site := get_xkcd().num) != latest_xkcd_in_dir:
        create_subdirectories(xkcd_directory, c.XKCD_SUBDIRECTORY_NAMES)

        print(f"Fetching new xkdcs from {latest_xkcd_in_site} to {latest_xkcd_in_dir}…")
        oldest_xkcd_in_dir = get_oldest_xkcd_in_dir(
            xkcd_directory / c.XKCD_SUBDIRECTORY_NAMES[0]
        )
        should_get_old_xkcd = oldest_xkcd_in_dir > latest_xkcd_in_dir

        for xkcd_num in range(latest_xkcd_in_site, latest_xkcd_in_dir, -1):
            if xkcd_num == 404:
                # xkcd 404 doesn't exist, so it needs to be skipped to avoid error 404
                continue
            if (should_get_old_xkcd and xkcd_num < oldest_xkcd_in_dir) or (
                not should_get_old_xkcd and xkcd_num > oldest_xkcd_in_dir
            ):
                xkcd = get_xkcd(str(xkcd_num))
                if xkcd.should_skip:
                    continue
                print(f"Storing xkcd number {xkcd_num}…")
                store_xkcd(xkcd_directory, xkcd)

        print(
            f"Done! {latest_xkcd_in_site - latest_xkcd_in_dir} new xkdcs successfully downloaded."
        )
    else:
        print("No new xkdc found.")


def get_xkcd_directory() -> Path:
    """
    Returns the directory where xkcds are saved. The directory is either read from a
    file "xkcd-path.txt" located in the "data" subdirectory of the "c.ROOT_PATH"
    directory, or the user is prompted to select the directory using a file dialog.
    If the file is not found or the selected directory is not valid, the function will
    continue to prompt the user until a valid directory is selected. The returned
    directory is stored in the file for future use.

    :return: Path to store xkcds.
    :rtype: Path
    """
    data_file_path = c.ROOT_PATH / "data/xkcd-path.txt"

    try:
        with open(data_file_path, "r+") as f:
            content = f.read().strip()
            path_in_file = Path(content)

            if content and path_in_file.exists():
                return path_in_file

            message = "Select the directory where you want to save the xkcds"
            print(message)
            selected_directory = filedialog.askdirectory(
                initialdir=c.ROOT_PATH, title=message
            )

            if selected_directory:
                f.seek(0)
                f.truncate()
                f.write(selected_directory)

                return Path(selected_directory)
            else:
                return get_xkcd_directory()
    except FileNotFoundError:
        print(f"The file '{data_file_path.stem}' could not be found.")


def create_subdirectories(root: Path, subdirectories: list[str]):
    """
    Create subdirectories within a root directory.

    :param root: The root directory where subdirectories will be created.
    :type root: Path
    :param subdirectories: List of subdirectory names to be created.
    :type subdirectories: list[str]
    """
    for subdirectory in subdirectories:
        (root / subdirectory).mkdir(exist_ok=True)


def get_latest_xkcd_in_dir(directory: str) -> int:
    """
    Returns the latest xkcd number stored in a directory by searching for the
    highest number in the file names.

    :param directory: A string representing the directory path.
    :return: An int representing the latest xkcd number. If no xkcd is found,
    returns 0 as default.
    """
    return max(
        (
            int(re.search(r"\d+", str(file)).group())
            for file in Path(directory).glob("*")
            if re.search(r"\d+", str(file))
        ),
        default=0,
    )


def get_oldest_xkcd_in_dir(directory: str) -> int:
    """
    Returns the oldest xkcd number stored in a directory by searching for the
    highest number in the file names.

    :param directory: A string representing the directory path.
    :type directory: str
    :return: An int representing the latest xkcd number. If no xkcd is found,
    returns -1 as default.
    :rtype: int
    """
    return min(
        (
            int(re.search(r"\d+", str(file)).group())
            for file in Path(directory).glob("*")
            if re.search(r"\d+", str(file))
        ),
        default=-1,
    )


def process_request(url: str) -> httpx.Response:
    """
    Performs a GET request to the specified URL and returns a httpx.Response object.

    It uses a httpx.Client object and sets the http2 parameter to True. In case of a
    failed request, the function retries the request up to 3 times with a 15 seconds
    sleep between each retry. If the last retry fails, an exception is raised.

    :param url: A string that represents the URL to be requested.
    :type url: str
    :return: A :class:`httpx.Response` object containing the response of the request.
    :rtype: :class:`httpx.Response`
    """
    with httpx.Client(http2=True) as client:
        max_retries = 3

        for retries in range(max_retries):
            try:
                res = client.get(url)
                res.raise_for_status()
                return res
            except Exception as e:
                if retries == max_retries - 1:  # last iteration
                    raise e

                time.sleep(15)


def get_xkcd(xkcd_num: str = "") -> models.Xkcd:
    """
    Retrieves an XKCD comic from the API.

    :param xkcd_num: The comic number to retrieve.
    If not specified, the latest comic will be retrieved.
    :type xkcd_num: str
    :return: A :class:`models.Xkcd` object representing the retrieved comic.
    :rtype: :class:`models.Xkcd`
    """
    res = process_request(c.XKCD_URL.format(xkcd_num))
    json = res.json()

    should_skip = True
    try:
        # the images of those xkcds that have extra_parts cannot be stored properly
        json["extra_parts"]
    except (Exception,):
        should_skip = False

    xkcd = models.Xkcd(
        num=json["num"], title=json["title"], img=json["img"], should_skip=should_skip
    )

    return xkcd


def store_xkcd(xkcd_directory: Path, xkcd: models.Xkcd):
    """
    Stores a xkcd comic.

    :param xkcd_directory: The directory where the comic should be stored.
    :type xkcd_directory: Path
    :param xkcd: The comic to store.
    :type xkcd: :class:`models.Xkcd`
    """
    forbidden_chars_in_file = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    title = xkcd.title.translate({ord(char): "" for char in forbidden_chars_in_file})
    base_name = f"{xkcd.num} ({title})"

    vignette_path = (
        xkcd_directory / Path(c.XKCD_SUBDIRECTORY_NAMES[0]) / f"{base_name}.png"
    )
    download_vignette(xkcd.img, vignette_path)

    explanation_path = (
        xkcd_directory / Path(c.XKCD_SUBDIRECTORY_NAMES[1]) / f"{base_name}.html"
    )
    download_explanation(c.XKCD_EXPLAIN_URL.format(xkcd.num), explanation_path)


def download_vignette(url: str, path: Path):
    """
    Download a xkcd comic vignette and save it to disk.

    :param url: The URL of the comic vignette.
    :type url: str
    :param path: The file path where the vignette should be saved.
    :type path: Path
    """
    img_data = process_request(url).content

    with open(path, "wb") as f:
        f.write(img_data)


def download_explanation(url: str, path: Path):
    """
    Download a xkcd comic explanation and save it to disk.

    :param url: The URL of the comic explanation.
    :type url: str
    :param path: The file path where the explanation should be saved.
    :type path: Path
    """
    explanation_data = process_request(url).content

    soup = bs4.BeautifulSoup(explanation_data, "html.parser")
    html_result_set = soup.select(
        '[style*="background-color: #FFFFFF; border: 1px solid #AAAAAA; color: black; font-size: 88%; line-height: 1.5em; margin: 0.5em 0 0.5em 1em; padding: 0.2em; text-align: center; width:98%;"] ~ p:not(:last-child)'
    )

    html_elements = [str(html_element) for html_element in html_result_set]
    explanation_html = "".join(html_elements)

    with open(path, "w", encoding="utf-8") as f:
        f.write(explanation_html)


if __name__ == "__main__":
    main()
