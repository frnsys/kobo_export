import json
import sqlite3

DB_PATH = 'KoboReader.sqlite'
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
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(QUERY_ITEMS)

    data = []
    for row in cur.fetchall():
        data.append({k: v for k, v in zip(KEYS, row)})

    cur.close()
    con.close()

    with open('kobo.json', 'w') as f:
        json.dump(data, f)