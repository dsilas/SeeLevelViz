FROM ubuntu:18.04

WORKDIR /seelevelviz

RUN apt update
RUN DEBIAN_FRONTEND="noninteractive" apt install -y gnupg lsb-release curl software-properties-common python3-dev python3-pip libx11-dev libgl-dev libgtk-3-dev qt5-default

RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt install -y libgdal-dev=2.4.2+dfsg-1~bionic0 gdal-bin=2.4.2+dfsg-1~bionic0 python-gdal=2.4.2+dfsg-1~bionic0 python3-gdal=2.4.2+dfsg-1~bionic0

COPY ./requirements.txt /seelevelviz/requirements.txt
RUN pip3 install --upgrade setuptools pip
RUN pip3 install -r /seelevelviz/requirements.txt

COPY ./src /seelevelviz/src

ENTRYPOINT ["python3", "src"]
