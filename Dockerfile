# ベースイメージとしてPythonを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libxss1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Playwrightの依存関係をインストール
RUN playwright install-deps && playwright install

# アプリケーションのソースコードをコンテナにコピー
COPY . .

# コンテナのエントリーポイントを設定
CMD ["python", "main.py"]