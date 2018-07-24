# mongo_fdw
FROM ubuntu:16.04
MAINTAINER Docker Newbee yenkuanlee@gmail.com

RUN apt-get -qq update

# Basic tool
RUN apt-get -qqy install sudo
RUN apt-get -qqy install python python-dev
RUN apt-get -qqy install vim
RUN apt-get -qqy install net-tools # ifconfig
RUN apt-get -qq update
RUN apt-get -qqy install aptitude
RUN apt-get -qqy install python-dev
RUN apt-get -qqy install python-setuptools
RUN apt-get -qqy install python-pip
RUN apt-get -qqy install git
RUN aptitude -y install build-essential

# Install Postgresql 9.6
RUN apt-get update 1>/dev/null && apt-get upgrade -y -q --no-install-recommends && apt-get install -y --no-install-recommends software-properties-common
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main"
RUN apt-get -qqy install wget
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get -qqy install postgresql-9.6
RUN apt-get -qqy install python-psycopg2
RUN apt-get -qqy install postgresql-server-dev-9.6
RUN sed -i 's/md5/trust/g' /etc/postgresql/9.6/main/pg_hba.conf
EXPOSE 5432

# Add localadmin user
RUN useradd -m localadmin && echo "localadmin:openstack" | chpasswd && adduser localadmin sudo
USER localadmin
RUN cd
CMD /bin/bash

# clone projet
RUN cd /home/localadmin && git clone https://github.com/yenkuanlee/IPTable
RUN cd /home/localadmin && git clone git://github.com/Kozea/Multicorn.git

# Install Multicorn
RUN cd /home/localadmin/Multicorn && dpkg --get-selections \| grep hold
USER root
RUN cd /home/localadmin/Multicorn && make && make install

# Install ipfs
RUN cp /home/localadmin/IPTable/ipfs_*fdw.py /usr/local/lib/python2.7/dist-packages/multicorn-1.3.4.dev0-py2.7-linux-x86_64.egg/multicorn && cp /home/localadmin/IPTable/ipfs /usr/local/bin && chmod 777 /usr/local/bin/ipfs
RUN pip install ipfsapi

USER localadmin
