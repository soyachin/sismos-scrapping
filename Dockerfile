FROM public.ecr.aws/lambda/python:3.12

RUN yum update -y && \
    yum install -y \
    unzip \
    libX11 \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXext \
    libXi \
    libXtst \
    cups-libs \
    libXScrnSaver \
    libXrandr \
    alsa-lib \
    atk \
    gtk3 \
    ipa-gothic-fonts \
    xorg-x11-fonts-100dpi \
    xorg-x11-fonts-75dpi \
    xorg-x11-utils \
    xorg-x11-fonts-cyrillic \
    xorg-x11-fonts-Type1 \
    xorg-x11-fonts-misc \
    xorg-x11-server-Xvfb \
    glibc-2.28

# chrome
RUN curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm -o google-chrome.rpm && \
    yum install -y ./google-chrome.rpm && \
    rm google-chrome.rpm

# chromedriver
RUN curl -SL https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -o chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver.zip

# python packages
RUN pip install --upgrade pip && \
    pip install selenium requests beautifulsoup4 boto3

# lambda code copy
COPY sismos.py ${LAMBDA_TASK_ROOT}

# 
CMD ["sismos.lambda_handler"]
