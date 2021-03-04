FROM python:3.9-slim-buster
WORKDIR /discord-bot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
CMD ["python3", "discord-bot.py"]