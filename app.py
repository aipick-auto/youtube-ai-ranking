import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="YouTube AI Ranking",
    page_icon="🔥",
    layout="wide"
)

# 버튼 색상 CSS
st.markdown("""
<style>
/* 영상 보기 버튼 - 빨간색 */
button[kind="secondary"] {
    background-color: #FF0000 !important;
    color: white !important;
    border: none !important;
}
button[kind="secondary"]:hover {
    background-color: #CC0000 !important;
    color: white !important;
}
/* 닫기 버튼 - 파란색 (primary) */
button[kind="primary"] {
    background-color: #0066CC !important;
    color: white !important;
}
button[kind="primary"]:hover {
    background-color: #004C99 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

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
                rank = item.get("rank", 0)
                title = item.get("title", "")
                channel = item.get("channel", "")
                view_count = item.get("viewCount", "")
                video_id = item.get("videoId", "")
                thumbnail_url = item.get("thumbnail", "")
                is_playing = st.session_state.get(f"play_{rank}", False)

                if is_playing and video_id and video_id != "dummy":
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                    st.markdown(f"### {rank}위 | {title}")
                    st.markdown(f"📺 {channel} | 👁️ {view_count}")
                    if st.button(
                        "✕ 영상 닫고 목록으로",
                        key=f"close_{rank}",
                        type="primary",
                        use_container_width=True
                    ):
                        st.session_state[f"play_{rank}"] = False
                        st.rerun()
                else:
                    cols = st.columns([1, 3])

                    with cols[0]:
                        if thumbnail_url:
                            st.image(thumbnail_url, use_container_width=True)

                    with cols[1]:
                        st.markdown(f"### {rank}위")
                        st.markdown(f"**{title}**")
                        st.markdown(f"📺 채널: {channel}")
                        st.markdown(f"👁️ 조회수: {view_count}")

                        if video_id and video_id != "dummy":
                            st.markdown("")
                            if st.button(
                                "🎬 영상 보기",
                                key=f"btn_{rank}",
                                use_container_width=True
                            ):
                                st.session_state[f"play_{rank}"] = True
                                st.rerun()

        st.divider()
        st.caption("데이터는 매일 자동으로 업데이트됩니다.")