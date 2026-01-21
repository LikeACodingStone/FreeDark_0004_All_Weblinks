'''
CHATGPT

1. 帮我写一个python脚本，
2. 大概就是在默认路径下面，读取chrome路径的bookmarks文件，
3. 所谓的默认路径就是自动识别当前代码在那个系统运行，只需要区分windows和ubuntu，bookmarks都是默认路径，默认安装
4. 然后自动生成chrome的可以直接导入的html文件，存放在当前python文件执行的统一级目录
5. 文件名字就叫做 google-bookmarks-date.html， date是当前的日期
'''

import os
import json
import platform
from datetime import datetime

def get_chrome_bookmarks_path():
    system = platform.system().lower()

    if system == "windows":
        user = os.environ.get("USERNAME")
        return fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    elif system == "linux":
        return os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
    else:
        raise RuntimeError("不支持的操作系统")

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
        add_date = node.get("date_added", "")
        f.write(f'{indent_str}<DT><A HREF="{url}">{name}</A>\n')

def main():
    bookmarks_path = get_chrome_bookmarks_path()

    if not os.path.exists(bookmarks_path):
        raise FileNotFoundError(f"未找到 Chrome Bookmarks 文件: {bookmarks_path}")

    with open(bookmarks_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    roots = data.get("roots", {})

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"google-bookmarks-{today}.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")
        for root in roots.values():
            write_bookmarks(root, f)

        f.write("</DL><p>\n")

    print(f"✅ 书签导出成功：{output_file}")

if __name__ == "__main__":
    main()
