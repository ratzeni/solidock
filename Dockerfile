FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y apt-utils rsync
RUN pip install -r requirements.txt
RUN solida info
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_8.x |  bash -
RUN apt-get install -y build-essential nodejs
RUN apt-get install -y libnss3-tools libgtk-3-0 libasound2 libxtst6 libgconf-2-4
RUN apt-get install -y x11-apps xvfb xauth x11-xserver-utils
#RUN xhost /private/tmp/com.apple.launchd.HsjNT77iTR/org.macosforge.xquartz:0
#COPY /private/tmp/com.apple.launchd.HsjNT77iTR/org.macosforge.xquartz:0 /code/
RUN npm install electron --save-dev

COPY . /code/

#


