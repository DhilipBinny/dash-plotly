FROM python:3.7

LABEL maintainer="Binny"

ENV PORT=3000

WORKDIR /app

ADD requirements.txt requirements.txt 

RUN pip install -r requirements.txt

ADD . .

EXPOSE 8050

CMD ["python", "index.py"]
