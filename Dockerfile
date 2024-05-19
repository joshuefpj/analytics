FROM ubuntu:20.04
LABEL Maintainer="Joshue"

ARG postgres_pass
ARG postgres_user
ARG postgres_db
ARG sender_email
ARG gmail_secret

# ARG DEBIAN_FRONTEND=noninteractive

ENV postgres_pass ${postgres_pass}
ENV postgres_user ${postgres_user}
ENV postgres_db ${postgres_db}
ENV sender_email ${sender_email}
ENV gmail_secret ${gmail_secret}

RUN apt-get update
RUN apt-get install python3 python3-pip libpq-dev python-dev cron -y

# Install psql
# RUN apt-get install -y postgresql

RUN pip3 install --upgrade pip

WORKDIR /usr/app

# Install required packages.
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add the remote files at root directory.
COPY ./analytic ./analytic

# Schedule script.
COPY ./py_cron ./
RUN chmod 644 ./py_cron
RUN crontab ./py_cron

CMD ["cron", "-f"]
