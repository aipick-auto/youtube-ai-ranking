import os
import json
from pathlib import Path

try:
    from googleapiclient.discovery import build
except ImportError:
    print("google-api-python-client가 설치되어 있지 않습니다.")
    print("pip install google-api-python-client 실행해주세요.")
    exit()

# 여기에 네 API 키 넣기
API_KEY = "AIzaSyDmp4z-RPP_DaHbWT8tqvuNjQqA_ZvKRNk"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def main():
    # 저장 폴더 만들기
    Path("data_art").mkdir(exist_ok=True)
    
    try:
        print("📊 전 세계 AI 아트 인기 영상 수집 중...")
        
        # YouTube API 클라이언트 생성
        youtube = build(
            YOUTUBE_API_SERVICE_NAME, 
            YOUTUBE_API_VERSION, 
            developerKey=API_KEY
        )
        
        # AI 아트 관련 키워드로 검색 (전 세계 기준, 조회수 높은 순)
        request = youtube.search().list(
            part="snippet",
            q="AI art OR Midjourney OR Flux OR DALL E OR Ideogram OR Recraft OR ComfyUI OR Flux Kontext",
            order="viewCount",
            maxResults=10,
            type="video"
        )
        
        response = request.execute()
        
        result = []
        video_ids = []
        
        # 영상 ID 모으기
        items = response.get("items", [])
        if not items:
            print("검색 결과가 없습니다.")
            return
        
        for item in items:
            video_id = item["id"].get("videoId")
            if video_id:
                video_ids.append(video_id)
        
        # 영상 상세 정보(조회수 등) 가져오기
        if video_ids:
            stats_request = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids)
            )
            stats_response = stats_request.execute()
            
            rank = 1
            
            # 데이터 정리
            for item in stats_response.get("items", []):
                snippet = item["snippet"]
                statistics = item["statistics"]
                
                title = snippet["title"]
                channel = snippet["channelTitle"]
                video_id = item["id"]
                thumbnail = snippet["thumbnails"]["medium"]["url"]
                
                # 조회수 포맷팅
                view_count = statistics.get("viewCount", "0")
                try:
                    views_int = int(view_count)
                    if views_int >= 100000000:
                        view_text = f"{views_int // 100000000}억회"
                    elif views_int >= 10000:
                        view_text = f"{views_int // 10000}만회"
                    else:
                        view_text = f"{views_int:,}회"
                except ValueError:
                    view_text = "조회수 없음"
                
                result.append({
                    "rank": rank,
                    "title": title,
                    "channel": channel,
                    "viewCount": view_text,
                    "thumbnail": thumbnail,
                    "videoId": video_id
                })
                
                rank += 1
        
        # 저장
        output_path = "data_art/latest.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 데이터 수집 완료! {output_path}")
        for item in result:
            print(f"  {item['rank']}위: {item['title']} ({item['channel']})")
        
    except Exception as e:
        import traceback
        print("에러 발생:")
        traceback.print_exc()
        print("\n기본 데이터로 저장합니다.")
        
        # 에러 시 기본 데이터
        result = []
        for i in range(1, 11):
            result.append({
                "rank": i,
                "title": f"AI 아트 인기 영상 {i}위",
                "channel": "AI 채널",
                "viewCount": "급상승 중",
                "thumbnail": f"https://via.placeholder.com/480x270/8b5cf6/ffffff?text=TOP{i}",
                "videoId": "dummy"
            })
        
        output_path = "data_art/latest.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("✅ 기본 데이터 저장 완료!")


if __name__ == "__main__":
    main()