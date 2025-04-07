import subprocess
import os
from pydub import AudioSegment
from openai import OpenAI
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
load_dotenv()


# 날짜 설정
KST = pytz.timezone('Asia/Seoul')
yesterday = datetime.now(KST) - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y%m%d")

# Whisper API 클라이언트
# 현재 파일의 상위 디렉토리로 이동
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 상위 디렉토리의 .env 파일 경로 지정
env_path = os.path.join(BASE_DIR, ".env")

# .env 파일 로드
load_dotenv(dotenv_path=env_path)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 저장 폴더 경로
folder_path = os.path.join(os.getcwd(), yesterday_str)

# URL 파일 경로
filename = os.path.join(folder_path, f"{yesterday_str}_url.txt")

# 1. URL 추출
video_info_list = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(" | ")
        channel = parts[0]
        url = parts[-1]
        video_info_list.append((channel, url))

print(f"총 {len(video_info_list)}개의 영상 처리 시작\n")

# 2. yt-dlp로 오디오 다운로드
def download_audio(video_url, output_path):
    command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        video_url
    ]
    subprocess.run(command, check=True)

# 3. 오디오 30분 단위로 자르기 (pydub)
def split_audio_by_minutes(input_path, chunk_length_min=20):
    audio = AudioSegment.from_file(input_path)
    chunk_ms = chunk_length_min * 60 * 1000
    chunks = []
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i+chunk_ms]
        chunk_path = f"{input_path.replace('.mp3', '')}_part{i//chunk_ms}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

# 4. Whisper API로 텍스트 변환
def transcribe_with_openai(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript

# 5. 반복 처리
for i, (channel_name, video_url) in enumerate(video_info_list):
    print(f"\n({i+1}/{len(video_info_list)}) 처리 중: {video_url}")

    audio_filename = os.path.join(folder_path, f"{channel_name}_{yesterday_str}.mp3")
    txt_filename = os.path.join(folder_path, f"{channel_name}_{yesterday_str}.txt")

    try:
        # (1) 오디오 다운로드
        download_audio(video_url, audio_filename)

        # (2) 30분 단위로 자르기
        chunks = split_audio_by_minutes(audio_filename)
        print(f"오디오 {len(chunks)}개 청크로 분할 완료")

        # (3) Whisper 변환 + 파일 저장
        all_text = ""
        for idx, chunk_file in enumerate(chunks):
            print(f"Whisper 처리 중: {chunk_file}")
            text = transcribe_with_openai(chunk_file)
            all_text += f"\n\n--- [Part {idx+1}] ---\n{text}"

        # (4) 최종 텍스트 파일 저장
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(all_text)

        print(f"저장 완료: {txt_filename}")

    except Exception as e:
        print(f"에러 발생: {e}")