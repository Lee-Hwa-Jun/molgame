# 기반 이미지: Python 3.9 슬림 버전
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# pip 최신 버전으로 업데이트
RUN pip install --upgrade pip

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Daphne 실행 (ASGI 서버)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]