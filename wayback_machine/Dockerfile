FROM python:3.9

WORKDIR /app

COPY . /app


RUN pip3 install requests beautifulsoup4 
RUN chmod +x /app/run_archiver.sh

VOLUME /app/result

CMD ["./run_archiver.sh"]

