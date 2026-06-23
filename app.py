import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="YouTube AI Ranking",
    page_icon="🔥",
    layout="wide"
)

# 제목
st.title("🔥 YouTube AI Ranking")
today = datetime.now().strftime("%Y년 %m월 %d일")
st.subheader(f"{today} AI 아트 인기 영상 TOP 50")

# 데이터 불러오기
data_path = Path("data_art/latest.json")

if not data_path.exists():
    st.error("데이터가 없습니다. collector_art.py를 먼저 실행해주세요.")
else:
    # JSON 파일 읽기
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 데이터가 없으면 에러
    if not data:
        st.warning("데이터가 비어있습니다.")
    else:
        # 랭킹 카드 보여주기
        for item in data:
            with st.container(border=True):
                cols = st.columns([1, 3])
                
                # 썸네일
                with cols[0]:
                    thumbnail_url = item.get("thumbnail", "")
                    if thumbnail_url:
                        st.image(thumbnail_url, use_container_width=True)
                
                # 정보
                with cols[1]:
                    rank = item.get("rank", 0)
                    title = item.get("title", "")
                    channel = item.get("channel", "")
                    view_count = item.get("viewCount", "")
                    video_id = item.get("videoId", "")
                    
                    # 순위
                    st.markdown(f"**{rank}위**")
                    
                    # 제목
                    st.markdown(f"### {title}")
                    
                    # 채널명
                    st.markdown(f"**채널:** {channel}")
                    
                    # 조회수
                    st.markdown(f"**조회수:** {view_count}")
                    
                    # 유튜브 링크 버튼
                    if video_id and video_id != "dummy":
                        youtube_url = f"https://youtu.be/{video_id}"
                        st.link_button(
                            "유튜브에서 보기", 
                            youtube_url,
                            use_container_width=False
                        )
        
        # 하단 정보
        st.divider()
        st.caption("데이터는 매일 자동으로 업데이트됩니다.")