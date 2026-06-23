# Dockerfile ← 프로젝트 루트에 생성
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main_crud:app", "--host", "0.0.0.0", "--port", "8000"]