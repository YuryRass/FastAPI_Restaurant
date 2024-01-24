FROM python:3.11

RUN mkdir /project

WORKDIR /project

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x docker/run.sh

CMD ["docker/run.sh"]