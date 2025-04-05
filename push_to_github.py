import os
from datetime import datetime, timedelta
import subprocess

# 1. 어제 날짜로 폴더 경로 설정
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")
folder_path = os.path.join(os.getcwd(), date_str)  # 예: ./20250405

# 2. 폴더가 존재하는지 확인
if not os.path.exists(folder_path):
    print(f"❌ 폴더 없음: {folder_path}")
    exit()

# 3. Git add (폴더 전체)
subprocess.run(["git", "add", folder_path])

# 4. Git commit
commit_message = f"{date_str} 뉴스 자동 업데이트 (CSV 및 워드클라우드 포함)"
subprocess.run(["git", "commit", "-m", commit_message])

# 5. Git pull로 충돌 방지
subprocess.run(["git", "pull", "--rebase", "origin", "main"])

# 6. Git push
subprocess.run(["git", "push", "origin", "main"])

print(f"\n📦 GitHub에 '{date_str}' 폴더 전체 커밋 및 푸시 완료!")
