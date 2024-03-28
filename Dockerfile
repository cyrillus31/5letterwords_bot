FROM python:3-alpine
WORKDIR  bot/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python server.py
