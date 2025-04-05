import os
import csv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime, timedelta
import re

# 1. API 키 로딩
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

# 2. 언어 모델 (Chat 기반)
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# 3. 한국어 요약 프롬프트
korean_prompt = PromptTemplate.from_template("""
다음 뉴스 기사 전체 내용을 정치 / 사회 / 국제 / 경제 / 기타 카테고리로 구분하여 요약해 주세요.

각 항목은 반드시 다음 형식을 따르세요:
정치: (요약)
사회: (요약)
국제: (요약)
경제: (요약)
기타: (요약)

뉴스 원문:
{text}

카테고리별 요약:
""")

# 4. 요약 체인
chain = load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    map_prompt=korean_prompt,
    combine_prompt=korean_prompt
)

# 5. 요약 함수
def summarize_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    docs = splitter.create_documents([text])
    return chain.invoke({"input_documents": docs})["output_text"]

# 6. 어제 날짜로 파일명 결정
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")

# 7. 처리할 채널 이름 목록
channels = ["SBS", "JTBC", "KBS", "MBC", "MBN", "채널A"]

# 8. 전체 CSV 저장을 위한 준비
csv_output_file = f"{date_str}_뉴스요약.csv"
with open(csv_output_file, "w", newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["방송사", "카테고리", "내용요약"])  # 헤더

    for channel in channels:
        input_filename = f"{channel}_{date_str}.txt"

        if not os.path.exists(input_filename):
            print(f"파일 없음: {input_filename}")
            continue

        print(f"\n요약 중: {input_filename}")

        try:
            with open(input_filename, "r", encoding="utf-8") as f:
                full_text = f.read()

            summary_text = summarize_text(full_text)

            # 줄 단위로 파싱 (예: 정치: . / 경제: .)
            for line in summary_text.strip().split("\n"):
                if ":" in line:
                    category, summary = line.split(":", 1)
                    clean_category = re.sub(r"[^\w가-힣]", "", category.strip())
                    writer.writerow([channel, category.strip(), summary.strip()])

            print(f"저장 완료 (CSV 병합): {channel}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

print(f"\n전체 뉴스 요약 CSV 파일 생성 완료: {csv_output_file}")
