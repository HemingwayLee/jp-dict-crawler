FROM python:3.8

RUN apt-get update && apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 sudo curl

RUN sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN sudo apt-get -y update
RUN sudo apt-get -y install google-chrome-stable

RUN mkdir -p /home/proj
WORKDIR /home/proj
COPY . .


RUN pip3 install -r requirements.txt
# RUN python3 stats.py
