FROM python:3.4
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' >> /etc/apt/sources.list.d/postgresql.list
RUN wget --no-sercheck-certificate -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O- | apt-key add -
RUN apt-get update && apt-get install -qq -y postgresql-client-9.6 cron

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x backup/backup.sh
RUN echo "0 3 * * 1 /usr/src/app/backup/backup.sh" >> mycron
RUN crontab mycron
RUN rm mycron
RUN service cron start
CMD ["cp", "-R", "/usr/src/app/static", "/data/static"]