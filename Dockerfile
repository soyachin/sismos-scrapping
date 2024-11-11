FROM public.ecr.aws/lambda/python:3.12

RUN apt-get update -y && \
    apt-get install -y \
    unzip \
    libx11-6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libxss1 \
    libxrandr2 \
    alsa-base \
    alsa-utils \
    atk \
    gtk3 \
    fonts-ipafont-gothic \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-utils \
    xfonts-cyrillic \
    xfonts-base \
    xvfb \
    libc6

# chrome
RUN curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    apt-get install -y ./google-chrome.deb && \
    rm google-chrome.deb

RUN curl -SL https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -o chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver.zipr/local/bin/ && \
    rm chromedriver.zip

RUN pip install --upgrade pip && \
    pip install selenium requests beautifulsoup4 boto3
RUN pip install --upgrade pip && \
    pip install selenium requests beautifulsoup4 boto3

# lambda code copy
COPY sismos.py ${LAMBDA_TASK_ROOT}

CMD ["sismos.lambda_handler"]
