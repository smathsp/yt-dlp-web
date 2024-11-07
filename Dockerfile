# 使用更小的 alpine 镜像
FROM python:3.10-alpine

# 设置工作目录
WORKDIR /app

# 安装基础依赖，包含 ffmpeg 用于视频处理
# 使用 `--no-cache` 防止缓存
RUN apk add --no-cache ffmpeg bash

# 安装 Python 依赖，添加 --no-cache-dir 防止缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建下载和 cookies 文件夹
RUN mkdir -p downloads cookies

# 暴露端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]
