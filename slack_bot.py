import requests
import json
from datetime import datetime, timedelta
import os


yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y%m%d") 
weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
weekday_name = weekdays[yesterday.weekday()]
date = yesterday_str[:4] + "년 " + yesterday_str[4:6] + "월 " + yesterday_str[6:8] + "일 " + weekday_name

url = 'https://hooks.slack.com/services/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'
headers = {"Content-type": "application/json"}
payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"""{date} 간추린 아침뉴스입니다!\n요약된 어제 뉴스는 링크를 통해 확인하세요:\n<https://newsalarm.streamlit.app/>"""
			}
		}
	]
}

r = requests.post(url, headers=headers, data=json.dumps(payload))
if r.status_code == 200:
    print("✅ 슬랙 메시지 전송 완료")
else:
    print(f"❌ 슬랙 전송 실패: {r.status_code} - {r.text}")

