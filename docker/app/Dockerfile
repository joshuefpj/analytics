FROM ubuntu:20.04
LABEL Maintainer="Josh"

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install --upgrade pip

WORKDIR /usr/app

# Install required packages.
COPY ../requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add the remote files at root directory.
COPY ../analytic ./

# Schedule script.
RUN crontab crontab

CMD ["crond", "-f"]
