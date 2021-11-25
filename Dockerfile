FROM ubuntu:16.04


RUN apt-get update -y && \
    
	apt-get install -y python-pip python-dev
	apt install python-pip pip install boto3


COPY ./requirements.txt /app/requirements.txt


WORKDIR /app


RUN pip install -r requirements.txt


EXPOSE 5000
COPY . /app


ENV FLASK_APP=app


ENV FLASK_RUN_PORT=5000
CMD [ "flask", "run", "--host", "0.0.0.0" ]

