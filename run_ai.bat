@echo off
cd /d "C:\youtube-trend\youtube ai ranking"
python collector_art.py
python make_shorts_art.py
python uploader_art.py