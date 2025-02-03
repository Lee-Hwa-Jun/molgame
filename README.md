## 📌 지원되는 Python 버전
Python **3.10 이상**이 필요합니다.

## 🛠️ .env 파일 예시
아래 내용을 참고하여 프로젝트 최상단에 `.env` 파일을 생성하세요.

```env
SERVER_IP=<your_server_ip>
SECRET_KEY=<your_secret_key>
```

## 📦 패키지 설치
아래 명령어를 실행하여 필요한 패키지를 설치하세요.

```bash
pip install -r requirements.txt
```

## 🚀 개발 서버 실행
개발 서버를 실행하려면 아래 명령어를 입력하세요.

```bash
python manage.py runserver --settings=config.settings.dev
```