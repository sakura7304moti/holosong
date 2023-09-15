"""
todo
・データベース作成
・追加
・検索
"""
import sqlite3
from . import const
dbname = const.sqlite_db()
#データベースの作成
def init():
    #アルバム別のデータベース
    """
    <holo_song_album>
    albumName:アルバム名
    artist:アーティスト名
    playlistLink:プレイリストのリンク
    date:公開日
    imageLink:アルバム画像のリンク
    """
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS holo_song_album(
                albumName STRING,
                artist STRING,
                playlistLink STRING,
                date STRING,
                imageLink STRING
                )
                """)
    conn.commit()
    conn.close()

    #曲別のデータベース
    """
    <holo_song_music>
    musicName:曲名
    artist:アーティスト名
    albumName:アルバム名
    musicLink:曲のリンク
    playlistLink:プレイリストのリンク
    imageLink:アルバム画像のリンク
    """
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS holo_song_music(
                musicName STRING,
                artist STRING,
                albumName STRING,
                musicLink STRING,
                playlistLink STRING,
                imageLink STRING
                )
                """)
    conn.commit()
    conn.close()

#アルバムのデータベースへの追加
def insert_album(albumName:str,artist:str,playlistLink:str,date:str,imageLink:str):
    #レコードの存在チェック
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    check_query = f"select * from holo_song_album where albumName = :albumName"
    cursor.execute(check_query,{'albumName':albumName})
    result = cursor.fetchall()
    if len(result) > 0:
        return False
    
    #追加クエリ
    query = """
    INSERT INTO holo_song_album 
    ( albumName , artist , playlistLink , date , imageLink) 
    VALUES ( :albumName , :artist , :playlistLink , :date ,:imageLink)
    """
    args = {
        'albumName':albumName,
        'artist' : artist,
        'playlistLink' : playlistLink,
        'date' : date,
        'imageLink' : imageLink
    }
    cursor.execute(query,args)
    conn.commit()
    conn.close()
    return True


#曲のデータベースへの追加
def insert_music(musicName:str,artist:str,albumName:str,musicLink:str,playlistLink:str,imageLink:str):
    #レコードの存在チェック
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    check_query = f"select * from holo_song_music where musicName = :musicName and albumName = :albumName"
    cursor.execute(check_query,{
        'musicName':musicName,
        'albumName':albumName
    })
    result = cursor.fetchall()
    if len(result) > 0:
        return False
    
    #追加クエリ
    query = """
    INSERT INTO holo_song_music 
    ( musicName , artist , albumName , musicLink , playlistLink , imageLink) 
    VALUES ( :musicName , :artist , :albumName , :musicLink ,:playlistLink , :imageLink)
    """
    args = {
        'musicName' : musicName,
        'artist' : artist,
        'albumName' : albumName,
        'musicLink' : musicLink,
        'playlistLink' : playlistLink,
        'imageLink' : imageLink
    }
    cursor.execute(query,args)
    conn.commit()
    conn.close()
    return True

#検索
#アルバム
def select_album():
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = "select * from holo_song_album"
    cursor.execute(query)
    results = cursor.fetchall()
    
    records = []
    for row in results:
        rec = const.HoloSongAlbum(*row)
        records.append(rec)
    
    conn.close()
    return records

def select_music():
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = "select * from holo_song_music"
    cursor.execute(query)
    results = cursor.fetchall()
    
    records = []
    for row in results:
        rec = const.HoloSongMusic(*row)
        records.append(rec)
    
    conn.close()
    return records