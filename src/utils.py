import functools
import json
import os
import re
import sys
from itertools import islice
import shutil

# Add the root directory to the system path
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_directory)

def copy_file_to_sync(source_path):
    """
    Copies a file to the ~/Sync directory.

    Args:
        source_path (str): The full or relative path of the file to copy.

    Returns:
        str: The destination path if successful, else None.
    """
    try:
        home_sync_dir = os.path.expanduser("~/Sync")
        os.makedirs(home_sync_dir, exist_ok=True)  # Ensure the destination directory exists

        filename = os.path.basename(source_path)
        destination_path = os.path.join(home_sync_dir, filename)

        shutil.copy2(source_path, destination_path)
        print(f"Copied '{filename}' to '{destination_path}'")

        return destination_path

    except Exception as e:
        print(f"Error copying file: {e}")
        return None

def slice_dict(d, start, end):
    """Slice a dictionary to include items from start index to end index (exclusive).

    Args:
        d (dict): The dictionary to slice.
        start (int): The starting index (inclusive).
        end (int): The ending index (exclusive).

    Returns:
        dict: A new dictionary with items from the specified range.
    """
    sliced_items = islice(d.items(), start, end)
    return dict(sliced_items)


def slice_cn_ch_dict(novel_name, ch_start_num, ch_end_num):
    """Slice Chinese chapters dictionary using chapters range.

    Args:
        novel_name (str): The name of the novel.
        ch_start_num (int): The starting chapter number (inclusive).
        ch_end_num (int): The ending chapter number (inclusive).

    Returns:
        dict: A dictionary containing the required chapters.
    """

    try:
        chinese_chapters_json = (
            f"docs/{novel_name}/jsons/cn_chapters/cn_chapters_all.json"
        )
        chinese_chapters_full_dict = read_json(chinese_chapters_json)

        chinese_chapters_required_dict = {}

        for num in range(ch_start_num, ch_end_num + 1):
            key = f"Chapter {num}"
            if key in chinese_chapters_full_dict:
                chinese_chapters_required_dict[key] = chinese_chapters_full_dict[key]
            else:
                print(f"Warning: {key} not found in the dictionary.")

        return chinese_chapters_required_dict

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        return {}

    except KeyError as key_error:
        print(f"Key error: {key_error} - Some chapters might be missing.")
        return {}


def extract_chapter_number(title):
    # Use regular expression to find the number after "Chapter"
    match = re.search(r"\d+", title)
    if match:
        chapter_number = f"Chapter {match.group(0)}"
        return chapter_number

    return title


def write_html(html, filename="test.html"):
    """Save the given HTML content to a file.

    Args:
        html (str): The HTML content to save.
        filename (str): The name of the file to save the HTML content to.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)


def pretty_write(text, file_name="temp.html"):

    soup = BeautifulSoup(text, "html.parser")

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(soup.prettify())


def read_html(file_name="temp.html"):
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def read_json(file_name="temp.json"):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(data, file_name="temp.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data written to {file_name}")


def log_var(*args):
    target_logger.info(*args)


def log_function_call(target_logger):
    def decorator_log_function_call(func):
        @functools.wraps(func)
        def wrapper_log_function_call(*args, **kwargs):
            # Log at the beginning of the function
            target_logger.info(f"Function: {func.__name__} started\n")

            # Execute the function
            result = func(*args, **kwargs)

            # Log at the end of the function
            target_logger.info(f"Function: {func.__name__} ended\n")

            return result

        return wrapper_log_function_call

    return decorator_log_function_call


def check_null(text):
    if text is None:
        print(f"{text} is None")
    else:
        print(f"{text} is not None")


def ensure_directory_exists(file_path):
    """
    Ensures that the directory for the given file path exists.
    If the directory does not exist, it will be created.

    Args:
        file_path (str): The file path for which to ensure the directory exists.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def docs_dirs_maker(novel_name):
    """
    Create the necessary directories for the novel.

    Args:
        novel_name (str): The name of the novel.
    """
    dirs_dict = {
        'epubs': [],
        'jsons': ['cn_chapters', 'en_chapters', 'it_chapters', 'mx_chapters'],
        'images': [],
        'htmls': ['cn_htmls', 'en_htmls', 'it_htmls', 'mx_htmls'],
    }
    for dir_name, sub_dirs in dirs_dict.items():
        main_dir = os.path.join("docs", novel_name, dir_name)
        os.makedirs(main_dir, exist_ok=True)
        for sub_dir in sub_dirs:
            os.makedirs(os.path.join(main_dir, sub_dir), exist_ok=True)
            print(f"Directory created: {os.path.join(main_dir, sub_dir)}")


if __name__ == "__main__":
    novel_name = "jsd"
    docs_dirs_maker(novel_name)
