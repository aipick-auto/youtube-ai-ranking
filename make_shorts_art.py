import os
import json
import requests
from datetime import datetime
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

# 아트 느낌 색상 (보라/핑크 계열)
RANK_COLORS = [
    (236, 72, 153),     # 1위 핑크
    (168, 85, 247),     # 2위 보라
    (139, 92, 246),     # 3위
    (124, 58, 237),     # 4위
    (99, 102, 241),     # 5위
    (56, 189, 248),     # 6위
    (34, 211, 238),     # 7위
    (45, 212, 191),     # 8위
    (251, 146, 60),     # 9위
    (248, 113, 113),    # 10위
]

FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/malgunbd.ttf"


def get_font(size, bold=False):
    try:
        path = FONT_BOLD_PATH if bold else FONT_PATH
        return ImageFont.truetype(path, size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()


def download_thumbnail(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return Image.open(BytesIO(res.content)).convert("RGBA")
    except:
        # 실패 시 빈 이미지 (보라 계열)
        return Image.new("RGBA", (480, 270), (139, 92, 246, 255))


def draw_centered_text(draw, y, text, font, fill="white", img_width=1920):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (img_width - text_width) // 2
    draw.text((x, y), text, fill=fill, font=font)


def draw_gradient_bg(img, color_top=(60, 10, 80), color_bottom=(20, 5, 40)):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h if h > 0 else 0
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def make_intro(data):
    """인트로 슬라이드 (16:9)"""
    img = Image.new("RGB", (1920, 1080))
    draw_gradient_bg(img, (80, 10, 120), (25, 5, 60))
    draw = ImageDraw.Draw(img)

    today = datetime.now().strftime("%Y년 %m월 %d일")

    # 상단 날짜
    draw_centered_text(draw, 80, today, get_font(44), fill=(230, 210, 255), img_width=1920)

    # 메인 타이틀
    draw_centered_text(draw, 160, "🔥 오늘의", get_font(78, bold=True), img_width=1920)
    draw_centered_text(draw, 240, "AI 아트 인기 급상승", get_font(68, bold=True), fill=(255, 200, 250), img_width=1920)
    draw_centered_text(draw, 320, "TOP 10", get_font(110, bold=True), fill=(255, 120, 200), img_width=1920)

    # 1~3위 썸네일 미리보기
    for i, item in enumerate(data[:3]):
        thumb = download_thumbnail(item["thumbnail"])
        if thumb:
            thumb_resized = thumb.resize((280, 158), Image.LANCZOS)
            x = 520 + i * 320
            y = 480

            # 테두리
            draw.rectangle([x - 5, y - 5, x + 285, y + 163], fill=RANK_COLORS[i])
            img.paste(thumb_resized, (x, y))

            # 순위 뱃지
            draw.rectangle([x, y, x + 55, y + 50], fill=RANK_COLORS[i])
            draw.text((x + 12, y + 5), str(i + 1), fill="white", font=get_font(32, bold=True))

            # 제목
            short_title = item["title"]
            if len(short_title) > 14:
                short_title = short_title[:14] + "..."
            draw.text((x, y + 175), short_title, fill="white", font=get_font(24))

    # 하단 문구
    draw_centered_text(draw, 780, "지금 바로 확인하세요! 👇", get_font(46), fill=(220, 190, 255), img_width=1920)

    # 채널명
    draw_centered_text(draw, 920, "📺 유튜브 AI 랭킹", get_font(38), fill=(200, 170, 240), img_width=1920)

    return img


def make_slide(rank, title, channel, view_count, thumb_url, color):
    """순위별 슬라이드 (16:9)"""
    img = Image.new("RGB", (1920, 1080))
    draw_gradient_bg(img, (70, 10, 110), (20, 5, 50))
    draw = ImageDraw.Draw(img)

    # 순위 뱃지
    badge_w = 380
    badge_h = 160
    badge_x = (1920 - badge_w) // 2
    badge_y = 80
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=40, fill=color)
    draw_centered_text(draw, badge_y + 25, f"TOP {rank}", get_font(90, bold=True), img_width=1920)

    # 썸네일
    thumb = download_thumbnail(thumb_url)
    if thumb:
        thumb_resized = thumb.resize((920, 518), Image.LANCZOS)
        thumb_x = (1920 - 920) // 2
        thumb_y = 280

        # 테두리
        draw.rectangle(
            [thumb_x - 5, thumb_y - 5, thumb_x + 925, thumb_y + 523],
            fill=color
        )
        # 그림자
        draw.rectangle(
            [thumb_x + 6, thumb_y + 6, thumb_x + 926, thumb_y + 524],
            fill=(0, 0, 0, 80)
        )
        img.paste(thumb_resized, (thumb_x, thumb_y))

    # 제목
    title_font = get_font(48, bold=True)
    if len(title) > 28:
        line1 = title[:28]
        rest = title[28:]
        if len(rest) > 28:
            line2 = rest[:28] + "..."
        else:
            line2 = rest
        draw_centered_text(draw, 820, line1, title_font, img_width=1920)
        draw_centered_text(draw, 880, line2, title_font, img_width=1920)
    else:
        draw_centered_text(draw, 850, title, title_font, img_width=1920)

    # 구분선
    line_y = 950
    draw.line([(600, line_y), (1320, line_y)], fill=(100, 70, 140), width=2)

    # 채널명
    draw_centered_text(draw, 980, f"🛠️ {channel}", get_font(40), fill=(220, 200, 255), img_width=1920)

    # 조회수
    draw_centered_text(draw, 1040, view_count, get_font(38), fill=(190, 170, 240), img_width=1920)

    return img


def make_outro():
    """아웃트로 슬라이드 (16:9)"""
    img = Image.new("RGB", (1920, 1080))
    draw_gradient_bg(img, (80, 15, 130), (25, 5, 60))
    draw = ImageDraw.Draw(img)

    # 메인 문구
    draw_centered_text(draw, 220, "📊", get_font(110), img_width=1920)
    draw_centered_text(draw, 360, "전체 랭킹은", get_font(62, bold=True), img_width=1920)
    draw_centered_text(draw, 450, "앱에서 확인하세요!", get_font(62, bold=True), fill=(255, 200, 250), img_width=1920)

    # 구분선
    draw.line([(700, 550), (1220, 550)], fill=(120, 80, 150), width=2)

    # 서브 문구
    draw_centered_text(draw, 620, "👍 구독 & 좋아요", get_font(48), fill=(220, 170, 255), img_width=1920)
    draw_centered_text(draw, 690, "매일 핫한 AI 아트 소식!", get_font(40), fill=(200, 180, 240), img_width=1920)

    # 채널명
    draw_centered_text(draw, 900, "📺 유튜브 AI 랭킹", get_font(38), fill=(200, 170, 240), img_width=1920)

    return img


def make_thumbnail(data):
    """썸네일 생성 (1280x720)"""
    img = Image.new("RGB", (1280, 720))
    draw_gradient_bg(img, (80, 10, 130), (25, 5, 60))
    draw = ImageDraw.Draw(img)

    # 타이틀
    draw_centered_text(draw, 30, "🔥 오늘의 AI 아트", get_font(72, bold=True), img_width=1280)
    draw_centered_text(draw, 130, "인기 급상승 TOP 10", get_font(72, bold=True), fill=(255, 200, 250), img_width=1280)

    # 날짜
    today = datetime.now().strftime("%Y.%m.%d")
    draw_centered_text(draw, 230, today, get_font(35), fill=(220, 190, 255), img_width=1280)

    # 상위 3개 썸네일
    for i, item in enumerate(data[:3]):
        thumb = download_thumbnail(item["thumbnail"])
        if thumb:
            thumb_resized = thumb.resize((370, 208), Image.LANCZOS)
            x = 30 + i * 410
            y = 340

            # 테두리
            draw.rectangle([x - 5, y - 5, x + 375, y + 213], fill=RANK_COLORS[i])
            img.paste(thumb_resized, (x, y))

            # 순위 뱃지
            draw.rectangle([x, y, x + 60, y + 55], fill=RANK_COLORS[i])
            draw.text((x + 15, y + 8), str(i + 1), fill="white", font=get_font(35, bold=True))

            # 제목
            short_title = item["title"]
            if len(short_title) > 14:
                short_title = short_title[:14] + "..."
            draw.text((x, y + 220), short_title, fill="white", font=get_font(25))

    # 하단 브랜딩
    draw_centered_text(draw, 660, "📺 유튜브 AI 랭킹", get_font(30), fill=(200, 170, 240), img_width=1280)

    img.save("thumbnail_art.png")
    print("✅ 커스텀 썸네일 생성 완료! thumbnail_art.png")


def create_shorts():
    """영상 전체 생성"""
    if not os.path.exists("data_art/latest.json"):
        print("에러: data_art/latest.json이 없습니다.")
        print("먼저 collector_art.py를 실행해주세요.")
        return

    with open("data_art/latest.json", "r", encoding="utf-8") as f:
        data = json.load(f)[:10]

    Path("temp_art").mkdir(exist_ok=True)
    clips = []

    # 1. 인트로 (4초)
    print("🎬 인트로 생성 중...")
    intro = make_intro(data)
    intro.save("temp_art/intro.png")
    clips.append(ImageClip("temp_art/intro.png").set_duration(4))

    # 2. 각 순위 슬라이드 (3초씩)
    for i, item in enumerate(data):
        print(f"  📌 {item['rank']}위 슬라이드 생성 중...")
        slide = make_slide(
            item["rank"],
            item["title"],
            item["channel"],
            item["viewCount"],
            item["thumbnail"],
            RANK_COLORS[i]
        )
        path = f"temp_art/slide_{i}.png"
        slide.save(path)
        clips.append(ImageClip(path).set_duration(3))

    # 3. 아웃트로 (4초)
    print("🎬 아웃트로 생성 중...")
    outro = make_outro()
    outro.save("temp_art/outro.png")
    clips.append(ImageClip("temp_art/outro.png").set_duration(4))

    # 4. 영상 합치기
    print("🎞️ 영상 합치는 중...")
    final = concatenate_videoclips(clips, method="compose")

    # 4-1. 배경음악 추가
    audio_path = "bgm.wav"
    if os.path.exists(audio_path):
        print("🎵 배경음악 추가 중...")
        audio = AudioFileClip(audio_path)
        if audio.duration > final.duration:
            audio = audio.subclip(0, final.duration)
        audio = audio.audio_fadein(2).audio_fadeout(2)
        final = final.set_audio(audio)
    else:
        print("⚠️ bgm.wav 파일이 없어 음악 없이 저장합니다.")

    # 5. 저장
    final.write_videofile(
        "youtube_ai_shorts.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    # 6. 썸네일 생성
    print("🎨 썸네일 생성 중...")
    make_thumbnail(data)

    print("=" * 50)
    print("🎉 영상 제작 완료! youtube_ai_shorts.mp4")
    print("🎨 썸네일 완료! thumbnail_art.png")
    print("=" * 50)


if __name__ == "__main__":
    create_shorts()