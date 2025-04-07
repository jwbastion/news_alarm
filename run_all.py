import subprocess
from datetime import datetime


# 실행 로그 남기기
with open("실행로그.txt", "a", encoding="utf-8") as f:
    f.write(f"실행됨: {datetime.now()}\n")

print("[1/6] 유튜브 영상 URL 수집 중...")
subprocess.run(["python", "miniproject.py"], check=True)

print("\n[2/6] Whisper로 텍스트 변환 중...")
subprocess.run(["python", "url_whisper.py"], check=True)

print("\n[3/6] LangChain으로 뉴스 요약 중...")
subprocess.run(["python", "summary.py"], check=True)

print("\n[4/6] 워드클라우드 생성 중...")
subprocess.run(["python", "generate_wordcloud.py"], check=True)

print("\n[5/6] GitHub에 자동 푸시 중...")
subprocess.run(["python", "git.py"], check=True)

print("\n[6/6] Slack Bot 전송 중...")
subprocess.run(["python", "slack_bot.py"], check=True)

print("\n전체 자동화 완료! GitHub 업로드 및 SlackBot 전송송 완료.")
