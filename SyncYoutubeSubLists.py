'''
1. current code folder have sub folder youtube 
2. traversal the youtube folder list the files ends with ".md"
3. if the contents in the md is like this,means need to update.
https://www.youtube.com/@bulianglin
https://www.youtube.com/@bestpartners
https://www.youtube.com/@%E4%B8%89%E5%80%8B%E6%B0%B4%E6%A7%8D%E6%89%8B
https://www.youtube.com/@aranshu0
https://www.youtube.com/@%E8%B1%90%E6%94%B6%E8%8F%AF%E5%A4%8F%E5%9F%BA%E7%9D%A3%E6%95%99%E6%9C%83
https://www.youtube.com/@laozhou77
'
4. update the file, and setting links for all these links with title,
for example
[bulianglin](https://www.youtube.com/@bulianglin)
5. if the file is already setting is this style. nothing to do with it.
6. give me the whole python code to implement above function, 
remember youtube folder is the same at the code file folder
7. making markdown preview showing as independent line for each channel.
'''

import os
import re
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOUTUBE_DIR = os.path.join(BASE_DIR, "youtube")

# plain youtube channel url (whole line)
PLAIN_URL = re.compile(r'^https://www\.youtube\.com/@\S+$')

# markdown formatted link
MARKDOWN_URL = re.compile(r'^\[.+?\]\(https://www\.youtube\.com/@.+?\)$')


def channel_title_from_url(url: str) -> str:
    name = url.split("@", 1)[1]
    return unquote(name)


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    output = []

    for line in lines:
        stripped = line.strip()

        # ignore empty lines
        if not stripped:
            output.append("\n")
            continue

        # ignore stray quote lines like: '
        if stripped == "'":
            changed = True
            continue

        # already markdown — keep
        if MARKDOWN_URL.match(stripped):
            output.append(stripped + "\n")
            continue

        # plain youtube link — convert
        if PLAIN_URL.match(stripped):
            title = channel_title_from_url(stripped)
            output.append(f"[{title}]({stripped})\n")
            changed = True
        else:
            output.append(line)

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(output)
        print(f"Updated: {path}")


def traverse_youtube():
    if not os.path.isdir(YOUTUBE_DIR):
        print("youtube folder not found")
        return

    for root, _, files in os.walk(YOUTUBE_DIR):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))


if __name__ == "__main__":
    traverse_youtube()
    print("Finished.")
