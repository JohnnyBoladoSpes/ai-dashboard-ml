FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader stopwords punkt wordnet omw-1.4

COPY . .

EXPOSE 9000

CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--reload-dir", "/app"]
