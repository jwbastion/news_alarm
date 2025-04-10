# 간추린 Morning News
  
## 개요
매일 오전 9시! 전날의 주요 뉴스를 빠르고 간단하게 확인할 수 있는 자동 봇 서비스  

SBS 8시 뉴스, KBS 9시 뉴스, MBC 뉴스데스크, JTBC 뉴스룸, 채널A 뉴스A, MBN 뉴스7 이상 6개 채널을 제공합니다.  

작업 스케줄러를 이용하여 자동으로 업로드합니다.

## 프로젝트 구조
### Tools
+ **Youtube URL**: Youtube Data API v3, PlayList
+ **Generate_Audio**: yt-dlp
+ **Audio Transcription**: OpenAI API Whisper-1
+ **News Summary**: OpenAI API GPT-4o
+ **WordCloud**: wordcloud
+ **News Website**: streamlit
 
### 주요 소스코드
| 파일명                     | 설명                                               |
| -------------------------- | -------------------------------------------------- |
| **`run_all.py`**           | 🚀 전체 코드 실행(자동화)                          |
| **`miniproject.py`**       | 🖥️ Youtube 뉴스 채널 Url 추출                     |
| **`url_whisper.py`**       | 🎞️ 영상 오디오 추출 및 텍스트 변환                 |
| **`summary.py`**           | ⚙️ ChatGPT 활용한 뉴스 요약                       |
| **`generate_wordcloud.py`**| 🔢 뉴스 주요 키워드 추출 및 워드클라우드 제작       |
| **`web.py`**               | 🧠 배포 위한 streamlit 활용한 웹페이지 구현        |
| **`slack_bot.py`**         | 🛜 배포된 뉴스 웹페이지 슬랙 앱 업로드             |

### 파일 구조
```
📂 20250407                          # 뉴스 데이터가 위치한 디렉토리(ex.4월 7일)
    └──📄 20250407_url.txt           # 방송사 6개 채널의 유튜브 뉴스 영상 url
    └──📄 SBS_20250407.mp3           # 영상에서 추출한 오디오 파일(6개 채널 동일)
    └──📄 SBS_20250407.txt           # 텍스트로 변환한 뉴스 스크립트(6개 채널 동일)
    └──📄 20250407_뉴스요약.csv       # 6개 채널에 대한 뉴스 요약
    └──📄 20250407_wordcloud.png     # 워드클라우드 이미지 파일
```

## 🚀 실행 방법

1️⃣ 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

2️⃣ 작업 스케줄러에서 `run_all.py`를 실행하여 자동화 봇을 시작합니다.

## 🔗 참조
+ **FFmpeg 설치**: [FFmpeg 설치 방법(Windows OS)](https://angelplayer.tistory.com/351)
