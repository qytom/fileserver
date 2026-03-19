FROM registry.cn-hangzhou.aliyuncs.com/library/python:3.8

# 设置工作目录
WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    git \
    openjdk-11-jdk \
    build-essential \
    python3-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装buildozer
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com buildozer

# 复制项目文件
COPY . /app

# 初始化buildozer
RUN buildozer init || true

# 构建APK
CMD ["buildozer", "android", "debug"]
