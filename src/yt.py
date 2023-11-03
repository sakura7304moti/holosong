import os
import yt_dlp
from tqdm import tqdm
import glob
from . import const

# プロジェクトの相対パス
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

music_path = os.path.join(base_path,'music')
if not os.path.exists(music_path):
    os.makedirs(music_path)
    
def get_url_list(playlist_url = 'https://music.youtube.com/playlist?list=PLzZYwYu_p6-W_7xYVv9nLIpGQj3dHI1BQ&si=LcmWwI2mPDjhN-VJ'):
    # オプションを設定
    ydl_opts = {
        'quiet': True,  # 出力を非表示
        'extract_flat': True,  # プレイリスト内の各動画を一つのリストに展開
        # その他のオプションは必要に応じて設定
    }

    # yt-dlpオブジェクトを生成
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # プレイリストからURLリストを取得
    with ydl:
        result = ydl.extract_info(playlist_url, download=False)

    if 'entries' in result:
        video_list = [entry['url'] for entry in result['entries']]
        return video_list
    else:
        print('プレイリストからエントリーが見つかりませんでした。')
        return None

def download(url:str):
    # ダウンロードオプションを設定
    ydl_opts = {
        'ignore-errors':True,
        'quiet': True,  # エラーメッセージの表示を無効にする
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(music_path,'%(title)s # %(uploader)s # %(id)s # %(upload_date)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 動画の情報を取得
        video_info = ydl.extract_info(url, download=False)

        # ダウンロード
        output_file = os.path.join(music_path, ydl.prepare_filename(video_info))
        print(f'output_file -> {output_file}')
        if not os.path.isfile(output_file+'.mp3'):
            ydl.download([url])
        else:
            print('skiped')
    
def get_music(path:str):
    file_name = os.path.basename(path)
    base_name, extension = os.path.splitext(file_name)
    split_list = base_name.split('#')
    if "" in split_list:
        split_list.remove("")
    rec = const.Music('','','','','')
    rec.file_name = base_name
    for index,sp in enumerate(split_list):
        if index == 0:
            rec.song_name = sp.strip()
        if index == 1:
            rec.member = sp.strip()
        if index == 2:
            rec.link = f'https://www.youtube.com/watch?v={sp.strip()}'
        if index == 3:
            rec.date = sp.strip()
    return rec

def get_music_list():
    records = []
    music_list = glob.glob(os.path.join(music_path,'*.mp3'))
    for path in music_list:
        rec = get_music(path)
        records.append(rec)
    return records