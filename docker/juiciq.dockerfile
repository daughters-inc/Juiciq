FROM python:3.9.1-buster

# copying local repo and installing requirements
RUN mkdir /apps
RUN mkdir /apps/juiciq
COPY . /apps/juiciq
RUN pip install -r /apps/juiciq/requirements.txt

# dependencies
RUN apt-get update
RUN apt-get -y install chromium unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# configs
ENV PYTHONUNBUFFERED=1
ENV LANG=en_US.utf8
EXPOSE 8000
#CMD cd /apps/juiciq && uvicorn juiciq:app --host 0.0.0.0 --port 8000
