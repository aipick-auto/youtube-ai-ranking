import os
import pickle
from datetime import datetime
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

TOKEN_FILE = "token_art.pickle"
APP_URL = "https://youtube-ai-ranking-a2tehafmcqhepmtw5mfyf6.streamlit.app/"
VIDEO_ID = "fIW5ZWdXBPM"


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
                "https://www.googleapis.com/auth/youtube",
                "https://www.googleapis.com/auth/youtube.force-ssl"
            ]
        )
        credentials = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(credentials, f)
    return credentials


def main():
    today = datetime.now().strftime("%Y년 %m월 %d일")

    desc = f"🔴▶️ 전체 50위 랭킹 보기\n\n"
    desc += f"{APP_URL}\n\n"
    desc += f"{today} AI 아트 인기 급상승 TOP 10\n\n"
    desc += f"#AI아트 #AI아트랭킹 #오늘의AI아트 #인기AI툴"

    print("--- 새 설명란 ---")
    print(desc)
    print("-----------------\n")

    confirm = input("이 설명란으로 업데이트할까요? (y/n): ")
    if confirm.lower() != "y":
        print("취소됨")
        return

    credentials = get_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    response = youtube.videos().list(
        part="snippet",
        id=VIDEO_ID
    ).execute()

    if not response["items"]:
        print("❌ 영상을 찾을 수 없습니다!")
        return

    snippet = response["items"][0]["snippet"]
    snippet["description"] = desc

    youtube.videos().update(
        part="snippet",
        body={
            "id": VIDEO_ID,
            "snippet": snippet
        }
    ).execute()

    print(f"✅ 설명란 업데이트 완료!")
    print(f"🔗 https://youtu.be/{VIDEO_ID}")


if __name__ == "__main__":
    main()