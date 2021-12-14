FROM centos:7

RUN mkdir /api
RUN yum install mariadb-server mariadb python3 python3-pip -y
RUN mysql_install_db --user=mysql

RUN sed -i '/\[mysqld\]/aport=3306' /etc/my.cnf

COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]
CMD ["./start.sh"]