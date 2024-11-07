from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import yt_dlp
import os
from threading import Thread

app = Flask(__name__)

# 下载文件目录
DOWNLOAD_FOLDER = "downloads"
COOKIES_FOLDER = "cookies"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(COOKIES_FOLDER, exist_ok=True)

# 下载进度存储
download_progress = {}

# 下载函数
def download_video(url, cookie_file=None):
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "progress_hooks": [download_progress_hook]
    }
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 下载进度回调
def download_progress_hook(d):
    if d["status"] == "downloading":
        download_progress["progress"] = d["_percent_str"]
        download_progress["speed"] = d.get("_speed_str", "N/A")
    elif d["status"] == "finished":
        download_progress["progress"] = "100%"
        download_progress["speed"] = "Done"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        cookie_file = None
        # 检查并保存 cookies 文件
        if "cookies" in request.files:
            cookie = request.files["cookies"]
            if cookie.filename:
                cookie_file = os.path.join(COOKIES_FOLDER, "cookies.txt")
                cookie.save(cookie_file)

        # 启动下载线程
        download_thread = Thread(target=download_video, args=(url, cookie_file))
        download_thread.start()
        return redirect(url_for("progress"))

    return render_template("index.html")

@app.route("/progress")
def progress():
    return render_template("progress.html", progress=download_progress)

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
