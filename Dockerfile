FROM python:3.11

RUN mkdir /project

WORKDIR /project

COPY requirements.txt /project

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /project

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0"]