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
    date:str
    member:str
    link:str
    song_name:str
    detail:str

    def __init__(
            self,
            date:str,
            member:str,
            link:str,
            song_name:str,
            detail:str,
    ):
        self.date =date
        self.member = member
        self.link = link
        self.song_name = song_name
        self.detail = detail

    def __str__(self):
        return {
            f"Date:{self.date}\n"
            f"Member:{self.member}\n"
            f"Link:{self.link}\n"
            f"SongName:{self.song_name}\n"
            f"Detail:{self.detail}\n"
        }
    
    def __dict__(self):
        return {
            "date":self.date,
            "member":self.member,
            "link":self.link,
            "songName":self.song_name,
            "detail":self.detail
        }