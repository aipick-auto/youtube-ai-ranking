import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="YouTube AI Ranking",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 YouTube AI Ranking")
today = datetime.now().strftime("%Y년 %m월 %d일")
st.subheader(f"{today} AI 아트 인기 영상 TOP 50")

data_path = Path("data_art/latest.json")

if not data_path.exists():
    st.error("데이터가 없습니다.")
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

                with cols[0]:
                    if thumbnail_url:
                        st.image(thumbnail_url, use_container_width=True)

                with cols[1]:
                    st.markdown(f"### {rank}위")
                    st.markdown(f"**{title}**")
                    st.markdown(f"📺 채널: {channel}")
                    st.markdown(f"👁️ 조회수: {view_count}")

                    if youtube_url:
                        st.link_button(
                            "▶ 유튜브에서 보기",
                            youtube_url,
                            use_container_width=False
                        )

        st.divider()
        st.caption("💡 유튜브 시청 후 브라우저 뒤로가기(←)를 누르면 랭킹으로 돌아옵니다.")