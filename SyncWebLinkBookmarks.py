'''
CHATGPT

1. 帮我写一个python脚本，
2. 大概就是在默认路径下面，读取chrome路径的bookmarks文件，
3. 所谓的默认路径就是自动识别当前代码在那个系统运行，只需要区分windows和ubuntu，bookmarks都是默认路径，默认安装
4. 然后自动生成chrome的可以直接导入的html文件，存放在当前python文件执行的统一级目录
5. 文件名字就叫做 google-bookmarks-date.html， date是当前的日期

6. 修改这一段代码，不要去默认的 home/xdrp/.config/google-chrome/Default/Bookmarks 
查找Bookmarks， 而是去 home/xdrp/.config/google-chrome，通过命令遍历查询出Booksmarks所在路径
7. 生成的导出的bookmarks文件，移动到当前文件夹下的bookmarks文件夹下面去
8. 对于生成的书签文件加上平台前缀，是windows还是linux，比如现在是linux，同时把同样的功能应用到windows平台
''' 


import os
import json
import platform
import shutil
from datetime import datetime


def get_platform_prefix():
    system = platform.system().lower()

    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        raise RuntimeError("Unsupported operating system")


def get_chrome_base_dir():
    system = platform.system().lower()

    if system == "windows":
        user = os.environ.get("USERNAME")
        return fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"

    elif system == "linux":
        return os.path.expanduser("~/.config/google-chrome")

    else:
        raise RuntimeError("Unsupported operating system")


def find_bookmarks_files():
    base_dir = get_chrome_base_dir()

    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Chrome config directory not found: {base_dir}")

    bookmarks_files = []

    for root, dirs, files in os.walk(base_dir):
        if "Bookmarks" in files:
            bookmarks_files.append(os.path.join(root, "Bookmarks"))

    if not bookmarks_files:
        raise FileNotFoundError("No Chrome Bookmarks files found")

    return bookmarks_files


def write_bookmarks(node, f, indent=1):
    indent_str = "    " * indent

    if node.get("type") == "folder":
        name = node.get("name", "Folder")

        f.write(f'{indent_str}<DT><H3>{name}</H3>\n')
        f.write(f'{indent_str}<DL><p>\n')

        for child in node.get("children", []):
            write_bookmarks(child, f, indent + 1)

        f.write(f'{indent_str}</DL><p>\n')

    elif node.get("type") == "url":
        name = node.get("name", "Untitled")
        url = node.get("url", "")

        f.write(f'{indent_str}<DT><A HREF="{url}">{name}</A>\n')


def export_bookmarks(bookmarks_paths, output_file):
    with open(output_file, "w", encoding="utf-8") as f:

        f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")

        for bookmarks_path in bookmarks_paths:

            print(f"Reading: {bookmarks_path}")

            with open(bookmarks_path, "r", encoding="utf-8") as bf:
                data = json.load(bf)

            roots = data.get("roots", {})

            for root in roots.values():
                write_bookmarks(root, f)

        f.write("</DL><p>\n")


def main():

    platform_prefix = get_platform_prefix()

    today = datetime.now().strftime("%Y-%m-%d")

    filename = f"{platform_prefix}-google-bookmarks-{today}.html"

    current_dir = os.path.dirname(os.path.abspath(__file__))

    bookmarks_dir = os.path.join(current_dir, "bookmarks")

    os.makedirs(bookmarks_dir, exist_ok=True)

    temp_output = os.path.join(current_dir, filename)

    bookmarks_files = find_bookmarks_files()

    export_bookmarks(bookmarks_files, temp_output)

    final_path = os.path.join(bookmarks_dir, filename)

    shutil.move(temp_output, final_path)

    print("")
    print("===================================")
    print(f"Export Success")
    print(f"File: {final_path}")
    print("===================================")


if __name__ == "__main__":
    main()