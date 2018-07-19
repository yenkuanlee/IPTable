# mongo_fdw
FROM ubuntu:16.04
MAINTAINER Docker Newbee yenkuanlee@gmail.com

RUN apt-get -qq update

# Basic tool
RUN apt-get -qqy install sudo
RUN apt-get -qqy install python python-dev
RUN apt-get -qqy install vim
RUN apt-get -qqy install net-tools # ifconfig

#1.Install Postgresql 9.6
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

#2.Install Git
RUN apt-get -qqy install git

# Add localadmin user
RUN useradd -m localadmin && echo "localadmin:openstack" | chpasswd && adduser localadmin sudo
USER localadmin
RUN cd
CMD /bin/bash

# clone proget
RUN cd /home/localadmin && git clone https://github.com/yenkuanlee/FoodResume
