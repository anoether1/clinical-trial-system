FROM python:3.11.4-slim-buster

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["./scripts/start.sh"]