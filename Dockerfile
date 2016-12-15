FROM python:latest
MAINTAINER lijian@ooclab.com

RUN apt-get update -y \
    && apt-get dist-upgrade -y \
    && apt-get install -y vim tree curl net-tools iputils-ping dstat htop \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install wheel ipython python-dateutil tornado sqlalchemy six wtforms \
        requests markdown pygments

COPY config/bashrc /root/.bashrc
COPY dist/pyeva-1.0.3.tar.gz /

RUN cd / && tar xf /pyeva-1.0.3.tar.gz && cd /pyeva-1.0.3/ && python setup.py install

VOLUME /work
WORKDIR /work

CMD ["bash"]
