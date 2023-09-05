from . import const
import requests
from bs4 import BeautifulSoup
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