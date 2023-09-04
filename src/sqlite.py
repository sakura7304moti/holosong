"""
CREATE DB
CREATE TABLE
INSERT DB
SEARCH
SEARCH COUNT
"""
import sqlite3
from . import const
dbname = const.sqlite_db()

"""
CREATE DB
"""

def init():
    # .dbを作成する
    conn = sqlite3.connect(dbname)
    conn.close()

    """
    CREATE TABLE
    """
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    # メインのテーブル
    cur.execute(
        """CREATE TABLE IF NOT EXISTS holotube(
        id INTEGER PRIMARY KEY,
        date STRING,
        member STRING,
        song_name STRING,
        detail STRING,
        cover INTEGER
        )
    """
    )
    conn.commit()

    #　サブのテーブル
    cur.execute(
        """CREATE TABLE IF NOT EXISTS holotubelink(
        id INTEGER,
        link STRING,
        tag STRING,
        title STRING
        )
    """
    )
    conn.commit()
    conn.close()

    