FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000"]
