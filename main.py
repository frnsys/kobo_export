"""
Usage:
- plug in your Kobo
- mount it: `sudo mount /dev/sda /media/usb/`
"""

import json
import sqlite3

DB_PATH = 'KoboReader.sqlite'
SAVE_PATH = 'kobo.json'
QUERY_ITEMS = (
    "SELECT "
    "Bookmark.VolumeID, "
    "Bookmark.Text, "
    "Bookmark.Annotation, "
    "Bookmark.ExtraAnnotationData, "
    "Bookmark.DateCreated, "
    "Bookmark.DateModified, "
    "content.BookTitle, "
    "content.Title, "
    "content.Attribution "
    "FROM Bookmark INNER JOIN content "
    "ON Bookmark.VolumeID = content.ContentID;"
)
KEYS = ['path', 'text', 'anno', 'extra_anno',
        'created', 'modified', 'book_title',
        'title', 'author']


if __name__ == '__main__':
    import sys
    # Allow override for DB_PATH
    args = sys.argv[1:]
    if args: DB_PATH = args.pop(0)
    if args: SAVE_PATH = args.pop(0)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(QUERY_ITEMS)

    try:
        data = json.load(open(SAVE_PATH))
    except FileNotFoundError:
        data = []
    for row in cur.fetchall():
        data.append({k: v for k, v in zip(KEYS, row)})

    cur.close()
    con.close()

    with open(SAVE_PATH, 'w') as f:
        json.dump(data, f)