# For more information, please refer to https://aka.ms/vscode-docker-python
FROM osgeo/gdal:ubuntu-full-3.2.1

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get -y install libpq-dev

COPY ./requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

COPY ./app /app/app
WORKDIR /app/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
COPY ./.cdsapirc /home/appuser/

ENTRYPOINT  [ "python3", "-m", "app" ]
