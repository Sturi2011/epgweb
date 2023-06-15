FROM debian:buster

MAINTAINER afohl <andreas@fohl.net>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y --force-yes install wget apt-transport-https
RUN apt-get -f install
RUN apt-get -y --force-yes install apache2 python3 python3-lxml
RUN mkdir /var/www/cgi-bin
RUN a2enmod cgi
RUN echo "\n<Directory /var/www/>\n        Options +ExecCGI\n        AddHandler cgi-script .py\n</Directory>\n" >> /etc/apache2/apache2.conf
RUN sed -i 's/\/usr\/lib/\/var\/www/g' /etc/apache2/conf-available/serve-cgi-bin.conf
RUN sed -i 's/index.cgi/\/cgi-bin\/epg.py/g' /etc/apache2/mods-enabled/dir.conf 
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY epg.py /var/www/cgi-bin/epg.py
COPY run.sh /run.sh
RUN rm /var/www/html/index.*
RUN chmod +x /var/www/cgi-bin/epg.py
RUN chmod +x /run.sh
CMD /run.sh && /usr/sbin/apachectl -D FOREGROUND

