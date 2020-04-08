FROM frolvlad/alpine-python-machinelearning

LABEL maintainer="Binny"

ENV PORT=3000

WORKDIR /app

ADD requirements.txt requirements.txt 

RUN pip install -r requirements.txt

ADD . .

EXPOSE 3000

CMD ["python", "index.py"]