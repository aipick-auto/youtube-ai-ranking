import os
import pickle
from datetime import datetime
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = "token_art.pickle"
APP_URL = "https://youtube-ai-ranking.streamlit.app/"

def get_credentials():
    credentials = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            credentials = pickle.load(f)

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json",
            [
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube",
                "https://www.googleapis.com/auth/youtube.force-ssl"
            ]
        )
        credentials = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(credentials, f)

    return credentials


def upload_video():
    if not os.path.exists("client_secrets.json"):
        print("에러: client_secrets.json 파일이 없습니다!")
        return
    if not os.path.exists("youtube_ai_shorts.mp4"):
        print("에러: youtube_ai_shorts.mp4 파일이 없습니다.")
        return

    credentials = get_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    today = datetime.now().strftime("%Y년 %m월 %d일")

    desc = f"🔴▶️ 전체 랭킹 보기\n\n"
    desc += f"{APP_URL}\n\n"
    desc += f"{today} AI 아트 인기 급상승 TOP 10\n\n"
    desc += f"#유튜브AI랭킹 #AI아트랭킹 #오늘의AI아트 #인기AI툴"

    title = f"{today} AI 아트 인기 급상승 TOP 10 🔥"

    print("📤 영상 업로드 중...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": desc,
                "tags": [
                    "유튜브AI랭킹",
                    "AI아트랭킹",
                    "오늘의AI아트",
                    "인기AI툴",
                    "AI아트"
                ],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "madeForKids": False
            }
        },
        media_body=MediaFileUpload("youtube_ai_shorts.mp4")
    )
    response = request.execute()
    video_id = response["id"]
    print(f"✅ 영상 업로드 성공! https://youtu.be/{video_id}")

    if os.path.exists("thumbnail_art.png"):
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload("thumbnail_art.png")
            ).execute()
            print("✅ 썸네일 등록 완료!")
        except:
            print("⚠️ 썸네일 등록 실패")

    print("💬 댓글 작성 중...")
    try:
        youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": f"전체 랭킹 보기\n{APP_URL}"
                        }
                    }
                }
            }
        ).execute()
        print("✅ 댓글 작성 완료!")
    except:
        print("⚠️ 댓글 작성 실패")

    print("=" * 40)
    print(f"🎉 완료! https://youtu.be/{video_id}")
    print("=" * 40)


if __name__ == "__main__":
    upload_video()