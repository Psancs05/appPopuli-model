FROM ubuntu

EXPOSE 8080

WORKDIR HOME

# WORKDIR /home
RUN apt update
RUN apt install python3-pip -y
RUN apt install cron -y
RUN apt install git -y
RUN apt update --fix-missing
RUN apt install ffmpeg  libxext6 libsm6 -y
# ffmpeg libsm6 libxext6  -y
RUN mkdir AppPopuli
WORKDIR /home/AppPopuli

COPY ./requirements.txt .
COPY ./src ./src
COPY ./data ./data

RUN apt-get update
RUN pip install -r requirements.txt

ENV FLASK_APP=src/backend.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]