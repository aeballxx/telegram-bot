FROM python:3.11-slim

WORKDIR /app

COPY bot.py .

RUN pip install python-telegram-bot

CMD ["python", "bot.py"]
