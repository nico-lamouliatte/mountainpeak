FROM python:3.12
LABEL authors="nicolas lamouliatte"

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]