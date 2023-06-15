# nextpvrepg
web epg container for nextpvr in docker container

Build with:

docker build  -t afohl/nextpvrepg .

Run with

docker run --name=nextpvrepg -d -t -p 80:80 -e "pin=0000" -e "server=http://192.168.0.1:8866" -e "scale=10" --restart=always  afohl/nextpvrepg

Parameters:

-e "pin=0000"                         Pin for NextPvr
-e "server=http://192.168.0.1:8866"   URL of NextPvr Server
-e "scale=10"                         Scale factor for Timeline
