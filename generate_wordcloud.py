import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from kiwipiepy import Kiwi
from PIL import Image
import numpy as np
from datetime import datetime, timedelta
import os

yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y%m%d")
date = yesterday_str[:4] + "/" + yesterday_str[4:6] + "/" + yesterday_str[6:8]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 예: project/
TXT_DIR = os.path.join(BASE_DIR, yesterday_str)  # 예: project/txt_files/

# 파일 읽기
file_paths = [
    os.path.join(TXT_DIR, f"SBS_{yesterday_str}.txt"),
    os.path.join(TXT_DIR, f"KBS_{yesterday_str}.txt"),
    os.path.join(TXT_DIR, f"MBC_{yesterday_str}.txt"),
    os.path.join(TXT_DIR, f"JTBC_{yesterday_str}.txt"),
    os.path.join(TXT_DIR, f"MBN_{yesterday_str}.txt"),
    os.path.join(TXT_DIR, f"채널A_{yesterday_str}.txt"),
]

all_text = ""

for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        all_text += file.read() + " "

# 1️⃣ 특수문자, 숫자 제거
all_text = re.sub(r"[^가-힣\s]", "", all_text)  # 한글과 공백만 남기기

# 2️⃣ Kiwipiepy를 사용한 명사 추출
kiwi = Kiwi()
tokens = kiwi.tokenize(all_text)

# 명사(NNG: 일반 명사, NNP: 고유 명사)만 추출
nouns = [token.form for token in tokens if token.tag in ["NNG", "NNP"]]

# 3️⃣ 불용어 제거
stopwords = set(
    ["것", "수", "그", "이", "저", "등", "더", "중", "개", "자", "때", "년", "한", "위","기자","시간","뉴스","정도"]
)
filtered_words = [
    word for word in nouns if word not in stopwords and len(word) > 1
]  # 한 글자 단어 제거

# 4️⃣ 단어 빈도수 계산
word_counts = Counter(filtered_words)
top_50_words = dict(word_counts.most_common(50))

mask = np.array(Image.open("cloud.png"))  # 하트 모양 이미지 로드

# 5️⃣ 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # Windows: "malgun.ttf", Mac: "AppleGothic"
    mask=mask,
    colormap="cool",
    background_color="white",
).generate_from_frequencies(top_50_words)

# 6️⃣ 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.figtext(
    0.5,
    0.1,
    f"{date} 키워드",
    ha="center",
    fontsize=16,
    color="black",
    fontname="Malgun Gothic",
    fontweight="500",
)
plt.axis("off")
plt.savefig(f"{yesterday_str}/{yesterday_str}_wordcloud.png", dpi=300, bbox_inches="tight")
plt.show()