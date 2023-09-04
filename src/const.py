import os
import pandas as pd
import yaml
import glob
import json

# プロジェクトの相対パス
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _url() -> dict:
    yaml_path = os.path.join(base_path, "options", "url.yaml")
    with open(yaml_path) as file:
        yml = yaml.safe_load(file)
    return yml

#URLまとめ
class UrlOption:
    def __init__(self):
        yml = _url()
        self.cover = yml['cover']
        self.ori = yml['ori']

#DBの保存先
def sqlite_db():
    return os.path.join(base_path,'song.db')

# QueryRecord---------------------------------------------
import sqlite3
import datetime

class SongQueryRecord:
    id:int
    date:str
    member:str
    song_name:str
    detail:str
    cover:int

    def __init__(
            self,
            id:int,
            date:str,
            member:str,
            song_name:str,
            detail:str,
            cover:int
    ):
        self.id = id
        self.date =date
        self.member = member
        self.song_name = song_name
        self.detail = detail
        self.cover = cover

    def __str__(self):
        return {
            f"Id:{self.id}\n"
            f"Date:{self.date}\n"
            f"Member:{self.member}\n"
            f"SongName:{self.song_name}\n"
            f"Detail:{self.detail}\n"
            f"Cover:{self.cover}"
        }
    
    def __dict__(self):
        return {
            "id":self.id,
            "date":self.date,
            "member":self.member,
            "songName":self.song_name,
            "detail":self.detail,
            "cover":self.cover
        }
    
class SongLink:
    id:int      #SongQueryRecordと共通
    link:str    #動画リンク
    tag:str     #動画・CD・ダウンロード/ストリーミング
    title:str   #YouTube?niconico?

    def __str__(self):
        # オブジェクトの文字列表現をカスタマイズ
        return f"id={self.id}, link={self.link}, tag={self.tag}, title={self.title}"

    def __dict__(self):
        # オブジェクトを辞書に変換
        return {
            "id": self.id,
            "link": self.link,
            "tag": self.tag,
            "title": self.title
        }