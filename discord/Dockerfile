FROM python:3.11-slim

WORKDIR /app

COPY src /app/

RUN python3 setup.py

CMD [ "python3", "main.py" ]