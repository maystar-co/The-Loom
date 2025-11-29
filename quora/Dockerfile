FROM python:3.9

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . /app


# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver



RUN pip3 install requests beautifulsoup4 selenium webdriver-manager
RUN chmod +x /app/run_quora_scraper.sh

VOLUME /app/result

CMD ["./run_quora_scraper.sh"]

