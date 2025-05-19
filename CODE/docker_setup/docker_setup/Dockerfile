# Use official Ubuntu base
FROM ubuntu:22.04

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install all essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    dnsutils \
    iproute2 \
    iputils-ping \
    net-tools \
    openssh-server \
    openssh-client \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    wget \
    iptables \
    jq \
    unzip \
    bzip2 \
    xz-utils \
    pciutils \
    libdbus-glib-1-2 \
    libxt6 \
    libxcb-shm0 \
    libxcb-dri3-0 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxrandr2 \
    lsb-release \
    xdg-utils \
    fonts-liberation \
    libappindicator3-1 \
    libdrm2 \
    libx11-xcb1 \
    libpci3 \
    openjdk-11-jre \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Create user with sudo and passwordless sudo access
RUN useradd -m -s /bin/bash selenium_grid && \
    echo "selenium_grid:kernel" | chpasswd && \
    usermod -aG sudo selenium_grid && \
    echo "selenium_grid ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH server
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 22/' /etc/ssh/sshd_config

# Switch to user and home directory
WORKDIR /home/selenium_grid

# Download and install browsers and drivers
RUN mkdir -p chrome chromedriver firefox && \
    CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chrome-linux64.zip" && \
    wget -q -O /tmp/chrome.zip "$CHROME_URL" && \
    unzip -q /tmp/chrome.zip -d /tmp/ && \
    mv /tmp/chrome-linux64/* chrome/ && \
    chmod +x chrome/chrome && \
    rm -rf /tmp/chrome.zip /tmp/chrome-linux64 && \
    CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip" && \
    wget -q -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL" && \
    unzip -q /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver chromedriver/ && \
    chmod +x chromedriver/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 && \
    FIREFOX_URL="https://ftp.mozilla.org/pub/firefox/releases/134.0b9/linux-x86_64/en-US/firefox-134.0b9.tar.bz2" && \
    wget -q -O /tmp/firefox.tar.bz2 "$FIREFOX_URL" && \
    tar -xjf /tmp/firefox.tar.bz2 -C firefox --strip-components=1 && \
    chmod +x firefox/firefox && \
    rm -rf /tmp/firefox.tar.bz2 && \
    GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz" && \
    wget -q -O /tmp/geckodriver.tar.gz "$GECKODRIVER_URL" && \
    tar -xzf /tmp/geckodriver.tar.gz -C /home/selenium_grid && \
    chmod +x /home/selenium_grid/geckodriver && \
    rm -rf /tmp/geckodriver.tar.gz

# Download Selenium Server
RUN wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.27.0/selenium-server-4.27.0.jar -O selenium-server.jar

# Setup Python virtual environment
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install selenium requests webdriver-manager && \
    pip freeze > requirements.txt

# Set environment variables
ENV PATH="/home/selenium_grid/venv/bin:/home/selenium_grid:/home/selenium_grid/chromedriver:/home/selenium_grid/firefox:/home/selenium_grid/chrome:${PATH}"
ENV CHROME_BIN=/home/selenium_grid/chrome/chrome
ENV FIREFOX_BIN=/home/selenium_grid/firefox/firefox
ENV GECKODRIVER_PATH=/home/selenium_grid/geckodriver

# Ensure correct ownership
RUN chown -R selenium_grid:selenium_grid /home/selenium_grid

# Expose ports
EXPOSE 22
EXPOSE 4444

# Switch to non-root user
USER selenium_grid

# Default command: open Bash shell
CMD ["/bin/bash"]

