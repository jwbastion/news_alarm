import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from kiwipiepy import Kiwi
from PIL import Image
import numpy as np
from datetime import datetime, timedelta
import os

# 어제 날짜로 폴더 경로 설정
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")
folder_path = os.path.join(os.getcwd(), date_str)
os.makedirs(folder_path, exist_ok=True)  # 폴더 없으면 생성

# 텍스트 파일 경로들
file_paths = [
    os.path.join(folder_path, f"{channel}_{date_str}.txt")
    for channel in ["SBS", "KBS", "MBC", "JTBC", "MBN", "채널A"]
]

all_text = ""

for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            all_text += file.read() + " "

# 1️⃣ 특수문자, 숫자 제거
all_text = re.sub(r"[^가-힣\s]", "", all_text)  # 한글과 공백만 남기기

# 2️⃣ Kiwipiepy로 명사 추출
kiwi = Kiwi()
tokens = kiwi.tokenize(all_text)
nouns = [token.form for token in tokens if token.tag in ["NNG", "NNP"]]

# 3️⃣ 불용어 제거
stopwords = set(["것", "수", "그", "이", "저", "등", "더", "중", "개", "자", "때", "년", "한", "위", "기자", "뉴스", "이번", "오전", "오후", "정도"])
filtered_words = [word for word in nouns if word not in stopwords and len(word) > 1]

# 4️⃣ 단어 빈도수 상위 50개 추출
word_counts = Counter(filtered_words)
top_50_words = dict(word_counts.most_common(50))

# 마스크 이미지 로드 (없을 경우 무시)
mask_path = os.path.join(os.getcwd(), "cloud.png")
mask = np.array(Image.open(mask_path)) if os.path.exists(mask_path) else None

# 5️⃣ 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # Windows 기준
    mask=mask,
    colormap="cool",
    background_color="white",
).generate_from_frequencies(top_50_words)

# 6️⃣ 저장 경로 → 폴더 안으로
output_path = os.path.join(folder_path, f"{date_str}_wordcloud.png")

# 7️⃣ 출력 및 저장
plt.figure(figsize=(7, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ 워드클라우드 저장 완료: {output_path}")
