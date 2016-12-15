FROM python:latest
MAINTAINER lijian@ooclab.com

RUN apt-get update -y \
    && apt-get dist-upgrade -y \
    && apt-get install -y vim tree curl net-tools iputils-ping dstat htop \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install wheel ipython python-dateutil tornado sqlalchemy six wtforms \
        requests markdown pygments

RUN mkdir /build/
COPY . /build/
RUN cd /build/ && python setup.py install && rm -rf /build/

VOLUME /work
WORKDIR /work

CMD ["bash"]
