import subprocess

print("[1/3] 유튜브 영상 URL 수집 중...")
subprocess.run(["python", "miniproject.py"], check=True)

print("\n[2/3] Whisper로 텍스트 변환 중...")
subprocess.run(["python", "url_whisper.py"], check=True)

print("\n[3/3] LangChain으로 뉴스 요약 중...")
subprocess.run(["python", "summary.py"], check=True)

print("\n전체 자동화 완료! '날짜_뉴스요약.csv' 파일을 확인하세요.")

subprocess.run(["python", "word_cloud.py"], check=True)

from datetime import datetime
with open("실행로그.txt", "a", encoding="utf-8") as f:
    f.write(f"실행됨: {datetime.now()}\n")
