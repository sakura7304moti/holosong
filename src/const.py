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

#pickleの保存先
def pickle_path():
    return os.path.join(base_path,'result.pickle')

#ホロメン一覧
def holoList():
    holo_path = os.path.join(base_path, "options", "holoMember.csv")
    df = pd.read_csv(holo_path)
    word_list = df["member"].tolist()
    return word_list

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
    
class HoloSongAlbum:
    albumName:str
    artist:str
    playlistLink:str
    date:str
    imageLink:str
    
    def __init__(self,albumName:str,artist:str,playlistLink:str,date:str,imageLink:str):
        self.albumName = albumName
        self.artist = artist
        self.playlistLink = playlistLink
        self.date = date
        self.imageLink = imageLink
        
    def __dict__(self):
        return {
            "albumName":self.albumName,
            "artist":self.artist,
            "playlistLink":self.playlistLink,
            "date":self.date,
            "imageLink":self.imageLink
        }
    
    def __str__(self):
        return f"Album Name: {self.albumName}\nArtist: {self.artist}\nPlaylist Link: {self.playlistLink}\nDate: {self.date}\nImage Link: {self.imageLink}"

    
class HoloSongMusic:
    musicName:str
    artist:str
    albumName:str
    musicLink:str
    playlistLink:str
    imageLink:str
    
    def __init__(self,musicName:str,artist:str,albumName:str,musicLink:str,playlistLink:str,imageLink:str):
        self.musicName = musicName
        self.artist = artist
        self.albumName = albumName
        self.musicLink = musicLink
        self.playlistLink = playlistLink
        self.imageLink = imageLink
        
    def __dict__(self):
        return {
            "musicName":self.musicName,
            "artist":self.artist,
            "playlistLink":self.playlistLink,
            "musicLink":self.musicLink,
            "playlistLink":self.playlistLink,
            "imageLink":self.imageLink
        }
    
    def __str__(self):
        return f"Music Name: {self.musicName}\nArtist: {self.artist}\nAlbum Name: {self.albumName}\nMusic Link: {self.musicLink}\nPlaylist Link: {self.playlistLink}\nImage Link: {self.imageLink}"
