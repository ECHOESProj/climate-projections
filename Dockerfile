FROM osgeo/gdal:ubuntu-full-3.2.1

RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get -y install libpq-dev

COPY ./requirements.txt /tmp/
COPY ./.cdsapirc /root/
RUN pip3 install -r /tmp/requirements.txt

COPY ./app /app/app
WORKDIR /app/

ENTRYPOINT  [ "python3", "-m", "app" ]
