import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import os

st.markdown(
    """
    <style>
    .news-title {
        font-size: 50px;  /* 타이틀 폰트 크기 */
        font-weight: bold;
        color: #333;
    }
    .broadcast {
        font-size: 40px;  /* 방송사 폰트 크기 */
        font-weight: bold;
        color: #333;
    }
    .category {
        font-size: 25px;  /* 카테고리 폰트 크기 */
        font-weight: bold;
        color: #555;
    }
    </style>
""",
    unsafe_allow_html=True,
)

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")

# 날짜 폴더 리스트 가져오기
available_dates = sorted([d for d in os.listdir(".") if os.path.isdir(d) and d.isdigit()])

# 사이드바에서 날짜 선택
selected_date = st.sidebar.selectbox("날짜를 선택하세요:", available_dates, index=len(available_dates)-1)

# 선택한 날짜로 폴더 경로 및 파일명 설정
date_str = selected_date
base_folder = selected_date

# CSV 파일 로드
file_path = f"{date_str}/{date_str}_뉴스요약.csv"
data = pd.read_csv(file_path)

# Streamlit 앱 제목
st.markdown(
    f'<div class="news-title">{date_str} 뉴스 요약</div>', unsafe_allow_html=True
)

st.write("---")

# Sidebar 설정
# st.sidebar.header("필터링 옵션")
broadcasting_companies = sorted(data["방송사"].unique())
categories = ["전체"] + list(data["카테고리"].unique())

# 방송사 체크박스 생성
selected_broadcastings = []
st.sidebar.subheader("방송사를 선택하세요:")
for company in broadcasting_companies:
    if st.sidebar.checkbox(company, key=f"broadcast_{company}"):
        selected_broadcastings.append(company)

# 카테고리 체크박스 생성
selected_categories = []
st.sidebar.subheader("카테고리를 선택하세요:")

# 상태 초기화
if "category_all" not in st.session_state:
    st.session_state["category_all"] = False
for category in categories[1:]:
    if f"category_{category}" not in st.session_state:
        st.session_state[f"category_{category}"] = False

# 콜백 함수: 전체 선택/해제 시 실행
def toggle_all_categories():
    new_state = not all(
        st.session_state[f"category_{c}"] for c in categories[1:]
    )
    for category in categories[1:]:
        st.session_state[f"category_{category}"] = new_state

selected_categories = []

# "전체" 체크박스 (on_change로 콜백 연결)
st.sidebar.checkbox(
    "전체",
    value=all(st.session_state[f"category_{c}"] for c in categories[1:]),
    key="category_all",
    on_change=toggle_all_categories
)

# 개별 카테고리 체크박스 생성
for category in categories[1:]:
    checked = st.sidebar.checkbox(
        category,
        value=st.session_state[f"category_{category}"],
        key=f"category_{category}"
    )
    if checked:
        selected_categories.append(category)

    
# 뉴스 요약 출력
broadcastings_str = ", ".join(selected_broadcastings)  # "JTBC, 채널A"
categories_str = ", ".join(selected_categories)  # "정치, 사회"
st.sidebar.subheader(f"방송사 \n{broadcastings_str}")
st.sidebar.subheader(f"카테고리\n {categories_str}")


# 필터링된 데이터 가져오기
if "전체" in selected_categories:
    filtered_data = data[data["방송사"].isin(selected_broadcastings)]
else:
    filtered_data = data[
        (data["방송사"].isin(selected_broadcastings))
        & (data["카테고리"].isin(selected_categories))
    ]

if not filtered_data.empty:
    image_path1 = f"{date_str}/{date_str}_wordcloud.png"  # 이미지 파일 경로
    image1 = Image.open(image_path1)
    st.image(image1, use_container_width=False, width=600)
    
    # 방송사별로 그룹화
    for broadcast, group in filtered_data.groupby("방송사"):
        first_row = True  # 첫 번째 행인지 체크

        for _, row in group.iterrows():
            if first_row:
                # 첫 번째 행에만 방송사 출력
                st.markdown(
                    f'<div class="broadcast">{row["방송사"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="category">{row["카테고리"]}</div>',
                    unsafe_allow_html=True,
                )
                first_row = False
            else:
                # 이후 행은 카테고리만 출력
                st.markdown(
                    f'<div class="category">{row["카테고리"]}</div>',
                    unsafe_allow_html=True,
                )
                first_row = False

            st.write(row["내용요약"])

        st.write("---")
else:

    image_path1 = f"{date_str}/{date_str}_wordcloud.png"  # 이미지 파일 경로
    image1 = Image.open(image_path1)
    # st.markdown(
    #     "<div style='text-align: center; font-size: 24px; color: #000;'>오늘의 키워드</div>",
    #     unsafe_allow_html=True
    # )
    st.image(image1, use_container_width=False, width=600)
