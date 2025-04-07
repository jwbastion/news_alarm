import subprocess
from datetime import datetime, timedelta
import pytz

# 날짜 설정
KST = pytz.timezone('Asia/Seoul')
yesterday = datetime.now(KST) - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y%m%d")

# Git으로 CSV와 PNG만 커밋
def commit_csv_png():
    try:
        # yesterday_str 디렉토리의 .csv와 .png 파일만 추가
        subprocess.run(["git", "add", f"{yesterday_str}/*.csv", f"{yesterday_str}/*.png"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add CSV and PNG files for {yesterday_str}"], check=True)
        # 원격 저장소로 푸시
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("CSV와 PNG 파일 커밋 완료!")
    except subprocess.CalledProcessError as e:
        print(f"Git 커밋 실패: {e}")

# 실행
commit_csv_png()