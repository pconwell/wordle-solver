# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.145.1/containers/python-3/.devcontainer/base.Dockerfile

ARG VARIANT="3.9-buster"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}


# set display port
ENV DISPLAY=:99

# install chrome/chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update
RUN apt-get install -y unzip google-chrome-stable chromium-driver

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install python packages from requirements.txt
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp