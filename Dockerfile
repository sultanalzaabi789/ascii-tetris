FROM python:3.11-slim

ENV TERM xterm-256color

WORKDIR /app
COPY . .

CMD ["python3", "main.py"]
