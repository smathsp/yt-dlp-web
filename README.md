# yt-dlp-web
使用docker部署yt-dlp网页版

## 使用方式

docker run -p 5000:5000 -v "$(pwd)/downloads:/app/downloads" -v "$(pwd)/cookies.txt:/app/cookies/cookies.txt" yt-dlp-web
