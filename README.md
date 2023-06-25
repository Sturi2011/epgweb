# nextpvrepg
epg display container for NextPVR, TVHeadend and MythTV  in docker container


dowload: 

mkdir ./epgweb
cd ./epgweb
git clone https://github.com/Sturi2011/epgweb.git


Build container with:

docker build  -t afohl/epgweb .


Run excample:

docker run --name=epgweb -d -t -p 80:80 -e "pin=0000" -e "server=http://192.168.0.1:8866" -e "servertype=NextPvr" -e "scale=10" --restart=always  afohl/epgweb


Parameters to start with NextPVR

pin=0000                         pin for NextPVR
server=http://1.1.1.1:8866       url NextPVR
scale=10                         timeresolution (optional)
offset=900                       reverse view time (optional)
shownowline=1                    enable/disable nowline (optional)
showtimeline=1                   enable/disable timeline (optional)
showflavor=1                     enable/disable display of servertype (optional)
servertype=NextPVR               servertype NextPVR
enabledebug=0                    enable/disable debug output (optional)


Parameters to start with TVHeadend

server=http://1.1.1.1:9981       url TVHeadend
scale=10                         timeresolution (optional)
offset=900                       reverse view time (optional)
shownowline=1                    enable/disable nowline (optional)
showtimeline=1                   enable/disable timeline (optional)
showflavor=1                     enable/disable display of servertype (optional)
servertype=TVHeadend             servertype TVHeadend
enabledebug=0                    enable/disable debug output (optional)


Parameters to start with MythTV

server=http://1.1.1.1:6654       url MythTV
scale=10                         timeresolution (optional)
offset=900                       reverse view time (optional)
shownowline=1                    enable/disable nowline (optional)
showtimeline=1                   enable/disable timeline (optional)
showflavor=1                     enable/disable display of servertype (optional)
servertype=MythTV                servertype MythTV
enabledebug=0                    enable/disable debug output (optional)

