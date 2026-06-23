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
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        st.warning("데이터가 비어있습니다.")
    else:
        for item in data:
            with st.container(border=True):
                cols = st.columns([1, 3])

                rank = item.get("rank", 0)
                title = item.get("title", "")
                channel = item.get("channel", "")
                view_count = item.get("viewCount", "")
                video_id = item.get("videoId", "")
                thumbnail_url = item.get("thumbnail", "")
                youtube_url = f"https://youtu.be/{video_id}" if video_id and video_id != "dummy" else ""

                # 썸네일 (HTML로 변경)
                with cols[0]:
                    if thumbnail_url:
                        st.markdown(
                            f'<a href="{youtube_url}" target="_blank">'
                            f'<img src="{thumbnail_url}" width="100%">'
                            f'</a>',
                            unsafe_allow_html=True
                        )

                # 정보
                with cols[1]:
                    # 순위 + 제목 (클릭 가능)
                    if youtube_url:
                        st.markdown(
                            f'**{rank}위** | '
                            f'<a href="{youtube_url}" target="_blank" '
                            f'style="color:white; text-decoration:none;">'
                            f'{title}</a>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(f"**{rank}위** | {title}")

                    st.markdown(f"📺 **채널:** {channel}")
                    st.markdown(f"👁️ **조회수:** {view_count}")

                    # 유튜브 버튼 (새 탭)
                    if youtube_url:
                        st.markdown(
                            f'<a href="{youtube_url}" target="_blank">'
                            f'<button style="background-color:#FF0000; color:white; '
                            f'border:none; padding:8px 16px; border-radius:5px; '
                            f'cursor:pointer; font-size:14px;">'
                            f'▶ 유튜브에서 보기</button></a>',
                            unsafe_allow_html=True
                        )

        st.divider()
        st.caption("데이터는 매일 자동으로 업데이트됩니다.")