#!/bin/bash
echo "[EPG]" > /var/www/cgi-bin/epg.conf
if [ -z "$pin" ]
then
      echo "pin='0000'" >> /var/www/cgi-bin/epg.conf
else
      echo "pin=$pin" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$server" ]
then
      echo "server='127.0.0.1'" >> /var/www/cgi-bin/epg.conf
else
      echo "server=$server" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$scale" ]
then
      echo "scale='10'" >> /var/www/cgi-bin/epg.conf
else
      echo "scale=$scale" >> /var/www/cgi-bin/epg.conf
fi
