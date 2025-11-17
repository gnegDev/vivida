FROM python:3.12
LABEL authors="gneg"

COPY . .

RUN pip3 install --upgrade pip -r requirements.txt

WORKDIR vivida

ENTRYPOINT ["python3", "app.py"]