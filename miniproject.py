import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import yt_dlp
import pytz

# 유튜브 API 설정
API_KEY = "AIzaSyBSpQd2xLiA0kh6PXZJbstGLuFvHoNsLTo"
youtube = build('youtube', 'v3', developerKey=API_KEY)
yt = "https://www.youtube.com/playlist?list="

# 재생목록 ID 리스트
channels = {
    "SBS": yt + "PLUHG6IBxDr3jKodEB2H_6DlFtXTVx0vf0",
    "JTBC": yt + "PL3Eb1N33oAXhNHGe-ljKHJ5c0gjiZkqDk",
    "KBS": yt + "PL9a4x_yPK_84HTyG0G2jUX9EkmKTtsCD8",
    "MBC": yt + "PLoMnIlrIuxWLJ4UHOpIFitKimYTj8Igzs",
    "채널A": yt + "PLkdmtGEOyYHIUevrSak3CWzA0OJ8714BS",
    "MBN": yt + "PLRI06Uh5cBHGVAQWXusHesQnK-wFChZ10"
}

# yt-dlp 설정
ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'playlist_items': '1'
}

# 날짜 설정 (어제 날짜 기준)
KST = pytz.timezone('Asia/Seoul')
yesterday = datetime.now(tz=KST) - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")  # 예: 20250403

# 저장 폴더 생성
folder_path = os.path.join(os.getcwd(), date_str)
os.makedirs(folder_path, exist_ok=True)

file_name = f"{date_str}_url.txt"
file_path = os.path.join(folder_path, file_name)

# 영상 정보 수집
video_lines = []

for channel_name, playlist_url in channels.items():
    print(f"\n채널: {channel_name}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if info['entries']:
                first_video = info['entries'][0]
                video_url = f"https://www.youtube.com/watch?v={first_video['id']}"
                video_title = first_video['title']
                line = f"{channel_name} | {video_title} | {video_url}"
                video_lines.append(line)
                print(f"{line}")
            else:
                print("재생목록에 영상이 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 텍스트 파일로 저장
with open(file_path, "w", encoding="utf-8") as f:
    for line in video_lines:
        f.write(line + "\n")

print(f"\n모든 채널의 URL을 '{file_path}' 파일로 저장했습니다.")
