FROM python:3.8.6

WORKDIR /usr/src/app

COPY . .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy", "crawl", "RebuildWorld"]
