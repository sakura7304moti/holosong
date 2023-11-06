from . import const
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import pickle
from yt_dlp import YoutubeDL
import re

urlModel = const.UrlOption()
cover_url = urlModel.cover
db_path = const.sqlite_db()

"""
データ収集
"""

def get_cover_songs():
    records = []

    # 指定したURLからHTMLを取得
    url = cover_url
    response = requests.get(url)

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    table_element = soup.find(id="table_edit_1 content_block_2")
    tr_elements = table_element.find("tbody").find_all("tr")

    # trループ
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        #各要素を取得
        td_date = td_elements[0].get_text().replace('/','-')
        td_member = td_elements[1].get_text()
        td_link = ''
        td_song_name = ''
        a_tag = td_elements[2].find("a")
        if a_tag is not None:
            td_link = a_tag.get("href")
            td_song_name = a_tag.get_text()

        td_detail = td_elements[3].get_text()
        rec = const.SongQueryRecord(td_date,td_member,td_link,td_song_name,td_detail)
        records.append(rec)
    return records

def get_original_songs():
    records = []
    response = requests.get('https://seesaawiki.jp/hololivetv/d/%a5%aa%a5%ea%a5%b8%a5%ca%a5%eb%a5%bd%a5%f3%a5%b0')
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('div',class_="wiki-section-3")
    for element in elements:
        text = element.text
        title = text.splitlines()[0]
        member_match = re.search(r"メンバー：(.+?)\n", text)
        if member_match:
            members = member_match.group(1)
        date_match = re.search(r"音源公開日：(\d{4}/\d{2}/\d{2})\n", text)
        if date_match:
            release_date = date_match.group(1).replace('/','-')
        a_tags = element.find_all('a', {'class': 'outlink', 'href': True, 'target': '_blank'})
        youtube_link = [a for a in a_tags if 'youtube' in a.text.lower()]
        if len(youtube_link) > 0:
            youtube_url = youtube_link[0]['href']
            rec = const.SongQueryRecord(release_date,members,youtube_url,title,'')
            records.append(rec)
    return records

#アルバム情報を取得
def get_albums():
    result_path = const.pickle_path()
    page_links = get_page_links()
    albums = []
    for page_link in tqdm(page_links):
        response = requests.get(page_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tag_list = [a for a in soup.find_all('a') if 'music/' in a['href']]
        for a in a_tag_list:
            try:
                #アルバム画像リンク,アルバム名,アーティスト名
                image_link = a.find('img')['src']
                name = a.find('h3').text
                artist = a.find('p').text

                #youtube musicのリンク取得
                music_page_link = a['href'].strip()
                sub_soup = BeautifulSoup(requests.get(music_page_link).text, 'html.parser')
                streaming_page_link = [a['href'] for a in sub_soup.find_all('a') if 'DOWNLOADやSTREAMINGはこちらから！' in a.text or 'DOWNLOAD and STREAMING links here!' in a.text][0].strip()
                if 'https:' not in streaming_page_link:
                    streaming_page_link =  'https:' + streaming_page_link
                st_soup = BeautifulSoup(requests.get(streaming_page_link).text, 'html.parser')
                try:
                    playlist_link = [a['href'] for a in st_soup.find_all('a') if 'https://music.youtube.com/playlist' in a['href']][0].strip().split('&src')[0]
                except:
                    #print('not found youtube URL')
                    next

                #発売日
                date_text = [i for i in sub_soup.find_all('p') if '価格' in i.text][0].find('strong').text
                year = date_text.split('年')[0]
                month = date_text.split('年')[1].split('月')[0]
                day = date_text.split('年')[1].split('月')[1].split('日')[0]
                date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
                
                #動画のURLのリストを取得
                musics = get_songs(playlist_link)

                time.sleep(0.1)
                albums.append([
                    name,
                    artist,
                    image_link,
                    date,
                    playlist_link,
                    musics
                ])
            except Exception as e:
                print(e)
            
            
            
    with open(result_path, mode="wb") as f:
        pickle.dump(albums, f)
    return albums
"""
SUB
"""


#プレイリストからURLとタイトルを取得
def get_songs(playlistUrl:str):
    musics = []
    with YoutubeDL() as y:
        res = y.extract_info(playlistUrl,download=False)
    for i in res['entries']:
        url = i['original_url']
        title = i['title']
        rec = [
            url,title
        ]
        musics.append(rec)
    return musics

#ページURLのリストを取得
def get_page_links():
    home_url = 'https://hololive.hololivepro.com/music'
    response = requests.get(home_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    total_pages = max([int(a.text) for a in soup.find_all('a',class_='page-numbers') if a.text.isdigit()])#ページ数を取得
    page_links = [f'https://hololive.hololivepro.com/music?paged={page_no}' for page_no in range(1,total_pages+1)]
    return page_links