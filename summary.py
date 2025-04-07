import os
import csv
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. API 키 로딩
load_dotenv()
# 현재 파일의 상위 디렉토리로 이동
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 상위 디렉토리의 .env 파일 경로 지정
env_path = os.path.join(BASE_DIR, ".env")

# .env 파일 로드
load_dotenv(dotenv_path=env_path)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. 언어 모델 (Chat 기반)
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# 3. 요약 프롬프트 설정
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

# 4. 요약 체인 생성
chain = load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    map_prompt=korean_prompt,
    combine_prompt=korean_prompt
)

# 5. 요약 함수 정의
def summarize_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    docs = splitter.create_documents([text])
    return chain.invoke({"input_documents": docs})["output_text"]

# 6. 날짜 및 경로 설정
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")
folder_path = os.path.join(os.getcwd(), date_str)
os.makedirs(folder_path, exist_ok=True)

# 7. 채널 목록
channels = ["SBS", "JTBC", "KBS", "MBC", "MBN", "채널A"]

# 8. CSV 저장 파일 경로
csv_output_file = os.path.join(folder_path, f"{date_str}_뉴스요약.csv")

# 9. 요약 결과 CSV로 저장
with open(csv_output_file, "w", newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["방송사", "카테고리", "내용요약"])

    for channel in channels:
        input_filename = os.path.join(folder_path, f"{channel}_{date_str}.txt")

        if not os.path.exists(input_filename):
            print(f"파일 없음: {input_filename}")
            continue

        print(f"\n요약 중: {input_filename}")

        try:
            with open(input_filename, "r", encoding="utf-8") as f:
                full_text = f.read()

            summary_text = summarize_text(full_text)

            for line in summary_text.strip().split("\n"):
                if ":" in line:
                    category, summary = line.split(":", 1)
                    writer.writerow([channel, category.strip(), summary.strip()])

            print(f"저장 완료: {channel}")
        except Exception as e:
            print(f"오류 발생: {e}")

print(f"\n전체 뉴스 요약 CSV 저장 완료 → {csv_output_file}")