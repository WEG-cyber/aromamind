# 使用官方 Python 輕量版作為基底
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼
COPY . .

# 設定環境變數 (Flask 預設通訊埠)
ENV PORT 8080

# 啟動指令 (使用 gunicorn)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
