#!/bin/bash
echo "[EPG]" > /var/www/cgi-bin/epg.conf
if [ -z "$pin" ]
then
      echo "pin=0000" >> /var/www/cgi-bin/epg.conf
else
      echo "pin=$pin" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$server" ]
then
      echo "server=127.0.0.1" >> /var/www/cgi-bin/epg.conf
else
      echo "server=$server" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$scale" ]
then
      echo "scale=10" >> /var/www/cgi-bin/epg.conf
else
      echo "scale=$scale" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$offset" ]
then
      echo "offset=900" >> /var/www/cgi-bin/epg.conf
else
      echo "offset=$offset" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$shownowline" ]
then
      echo "shownowline=1" >> /var/www/cgi-bin/epg.conf
else
      echo "shownowline=$shownowline" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$showtimeline" ]
then
      echo "showtimeine=1" >> /var/www/cgi-bin/epg.conf
else
      echo "showtimeline=$showtimeline" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$showflavor" ]
then
      echo "showflavor=0" >> /var/www/cgi-bin/epg.conf
else
      echo "showflavor=$showflavor" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$enabledebug" ]
then
      echo "enabledebug=0" >> /var/www/cgi-bin/epg.conf
else
      echo "enabledebug=$enabledebug" >> /var/www/cgi-bin/epg.conf
fi
if [ -z "$servertype" ]
then
      echo "servertype=NextPvr" >> /var/www/cgi-bin/epg.conf
else
      echo "servertype=$servertype" >> /var/www/cgi-bin/epg.conf
fi
