FROM python:3.4

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["cp", "-R", "/usr/src/app/static", "/data/static"]