import subprocess
from datetime import datetime

print("[1/5] 유튜브 영상 URL 수집 중...")
subprocess.run(["python", "miniproject.py"], check=True)

print("\n[2/5] Whisper로 텍스트 변환 중...")
subprocess.run(["python", "url_whisper.py"], check=True)

print("\n[3/5] LangChain으로 뉴스 요약 중...")
subprocess.run(["python", "summary.py"], check=True)

print("\n[4/5] 워드클라우드 생성 중...")
subprocess.run(["python", "wordcloud.py"], check=True)

# 실행 로그 남기기
with open("실행로그.txt", "a", encoding="utf-8") as f:
    f.write(f"실행됨: {datetime.now()}\n")

# GitHub 자동 커밋 & 푸시
print("\n[5/5] GitHub에 자동 푸시 중...")
import push_to_github

print("\n전체 자동화 완료! 생성된 CSV, 워드클라우드 파일 확인 및 GitHub 업로드 완료.")
