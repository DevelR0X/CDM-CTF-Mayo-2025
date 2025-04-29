FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    unzip \
    libnss3 \
    libxss1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY visitor.py .

RUN pip install --no-cache-dir selenium chromedriver-autoinstaller

ENV TARGET_URL="http://server"

CMD ["python", "visitor.py"]
