FROM ubuntu:20.04
LABEL Maintainer="Joshue"

# Environment vars.
ARG postgres_pass
ARG postgres_user
ARG postgres_db
ARG postgres_host
ARG sender_email
ARG gmail_secret

ENV postgres_pass ${postgres_pass}
ENV postgres_user ${postgres_user}
ENV postgres_db ${postgres_db}
ENV postgres_host ${postgres_host}
ENV sender_email ${sender_email}
ENV gmail_secret ${gmail_secret}

# Update and libs install.
RUN apt-get update
RUN apt-get install python3 python3-pip libpq-dev python-dev cron -y
RUN pip3 install --upgrade pip

WORKDIR /usr/app

# Install required packages.
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add the remote files at root directory.
COPY ./analytic ./analytic

# Schedule script.
COPY ./py_cron /etc/cron.d/crontab
RUN chmod 644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
