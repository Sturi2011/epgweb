#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#'''
# Custom Web EPG Server for Nextpvr and TVHeadend
#
# Copyright (c) 2023 Andreas Fohl <andreas@fohl.net>
# Under GPL V3 License
#
# https://github.com/sturi2011/nextpvrepg
#'''
import cgi
import urllib.request
import urllib.parse
import hashlib
import time
import calendar
import sys
import os 
from lxml import etree
parser=etree.XMLParser(recover=True)
import configparser
from array import *
import cgi
import datetime
import json
#ReadConfig
config = configparser.ConfigParser()
config.sections()
config.read('epg.conf')
sid=""
pin=config['EPG']['pin']
server=config['EPG']['server']
scale=int(config['EPG']['scale'])
offset=int(config['EPG']['offset'])*-1
shownowline=(config['EPG']['shownowline'])
showtimeline=(config['EPG']['showtimeline'])
showflavor=(config['EPG']['showflavor'])
servertype=(config['EPG']['servertype'])
enabledebug=(config['EPG']['enabledebug'])
if servertype == 'NextPvr':     
    stype=0
elif servertype == 'TVHeadend':
    stype=1 
elif servertype == 'MythTV':
    stype=2 
else: 
    stype=0

  
#Common Functions
def PrintHead(lang):
    print('''Content-Type: text/%s; charset=utf-8\n'''% (lang))
def PrintHeader():
    print('''<!DOCTYPE html><html>
 <head>
  <title>EPG</title>
  <link rel="stylesheet" href="/cgi-bin/epg.py?page=epgcss">
  <script>
        function showinfo(elementId) {
            var elem = document.getElementById("recordwindow");
            elem.style.display = "block";
            var elem = document.getElementById("recorddetail");
            elem.innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=epg_detail&eventId=" + elementId + "' width=100%  height=300px></object>"
            elem.style.display = "block";
            var rbutton = document.getElementById("recordbutton");
            var cbutton = document.getElementById("closebutton");
            cbutton.innerHTML="<br><a href='javascript:hideinfo()'>Schlie&szlig;en</a>";
            rbutton.innerHTML="<br><a href='javascript:record("+elementId+")'>Aufnehmen</a>";
            rbutton.style.display="block";
            cbutton.style.display="block";
        }
        function showinfomythtv(channel,starttime,endtime,callsign,title) {
            var elem = document.getElementById("recordwindow");
            elem.style.display = "block";
            var elem = document.getElementById("recorddetail");
            elem.innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=epg_detail&channel=" + channel + "&starttime=" + starttime+ "' width=100%  height=300px></object>"
            elem.style.display = "block";
            var rbutton = document.getElementById("recordbutton");
            var cbutton = document.getElementById("closebutton");
            cbutton.innerHTML="<br><a href='javascript:hideinfo()'>Schlie&szlig;en</a>";
            rbutton.innerHTML="<br><a href='javascript:recordmythtv(`"+channel+"`,`"+starttime+"`,`"+endtime+"`,`"+callsign+"`,`"+title+"`)'>Aufnehmen</a>";
            rbutton.style.display="block";
            cbutton.style.display="block";
        }
        function showinfodel(elementId,recordId) {
            var elem = document.getElementById("recordwindow");
            elem.style.display = "block";
            var elem = document.getElementById("recorddetail");
            elem.innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=epg_detail&eventId=" + elementId + "' width=100%  height=300px></object>"
            elem.style.display = "block";
            var rbutton = document.getElementById("recordbutton");
            var cbutton = document.getElementById("closebutton");
            cbutton.innerHTML="<br><a href='javascript:hideinfo()'>Schlie&szlig;en</a>";
            rbutton.innerHTML="<br><a href=javascript:recorddel('"+recordId+"')>Abbrechen</a>";
            rbutton.style.display="block";
            cbutton.style.display="block";
        }
        function showinfodelmythtv(channel,starttime,endtime,callsign,title) {
            var elem = document.getElementById("recordwindow");
            elem.style.display = "block";
            var elem = document.getElementById("recorddetail");
            elem.innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=epg_detail&channel=" + channel + "&starttime=" + starttime+ "' width=100%  height=300px></object>"
            elem.style.display = "block";
            var rbutton = document.getElementById("recordbutton");
            var cbutton = document.getElementById("closebutton");
            cbutton.innerHTML="<br><a href='javascript:hideinfo()'>Schlie&szlig;en</a>";
            rbutton.innerHTML="<br><a href='javascript:recorddelmythtv(`"+channel+"`,`"+starttime+"`)'>Abbrechen</a>";
            rbutton.style.display="block";
            cbutton.style.display="block";
        }
        function record(elementId) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recordevent&eventId=" + elementId + "' width='100%'></object>"
            var rbutton = document.getElementById("recordbutton")
            rbutton.style.display = "none";
        }
        function recordmythtv(channel,starttime,endtime,callsign,title) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recordevent&starttime=" + starttime + "&endtime=" + endtime + "&channel=" + channel + "&callsign=" + callsign + "&title=" + title + "' width='100%'></object>"
            var rbutton = document.getElementById("recordbutton")
            rbutton.style.display = "none";
        }
        function recorddel(elementId) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recorddelete&eventId=" + elementId + "' width='100%'></object>"
            var rbutton = document.getElementById("recordbutton")
            rbutton.style.display = "none";
        }
        function recorddelmythtv(channel,starttime) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recorddelete&channel=" + channel + "&starttime=" + starttime + "' width='100%'></object>"
            var rbutton = document.getElementById("recordbutton")
            rbutton.style.display = "none";
        }
        function hideinfo() {
            var elem = document.getElementById("recordwindow");
            elem.style.display = "none";
            var elem = document.getElementById("recordbutton");
            elem.style.display = "none";
            var elem = document.getElementById("closebutton");
            elem.style.display = "none";
            location.reload();
        }
  </script>
 </head>
<body>
<div title="Details" class="info" id="recordwindow">
<div title="Details" class="inforec" id="recorddetail"></div>
<div class="recordbutton" id="recordbutton"></div>
<div class="closebutton" id="closebutton"></div>
</div>''')
def PrintFooter():
    print('''</body></html>''')
def PrintEPGCSS():
    PrintHead('css')
    print('''body {
  background-color: #000000;
  font-family: Arial;
  margin: 0px;
  }
  
  a{
  text-decoration: none;
  color: #000000;
  }
  
  .timecode{
  font-size:10px;
  color:#ffffff;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  valign:top;
  }
  
  .timecodehour{
  font-size:14px;
  color:#ffffff;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  font-wight:bold;
  }
  
  .chanellogo {
  color: #ffffff;
  overflow:hidden;
  position: sticky;
  width: 66px;
  left: 0px;
  top: auto;
  background-color: #333333;
  z-index: 100;
  }

  .pvrflavor {
  font-size:10px;
  color:#ffffff;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  overflow:hidden;
  position: sticky;
  width: 66px;
  left: 0px;
  top: auto;
  background-color: #333333;
  z-index: 100;
  }

  .nowline {
  width:3px;
  background-Color:red;
  top:0px;
  z-index:75;
  position:absolute;
  opacity: 0.3;
  }
  
  .timeline10p {
  background-color: #333333;
  height:10px;
  position: relative;
  }

  .timeline20p {
  background-color: #333333;
  height:20px;
  position: relative;
  }
  
  .timelinemarker10p {
  width:1px; 
  height:10px;
  position: relative; 
  background-Color:#ffffff;
  }

  .timelinemarker20p {
  width:1px; 
  height:20px;
  position: relative; 
  background-Color:#ffffff;
  }
  
  .epgtxt {
  padding-left:3px;
  }
  
  table{
  border-collapse: separate;
  border-spacing: 0;
  }
  
  .epgrow{
  vertical-align: top;
  width: 100%;
  height: 100%;
  display: inline-flex;
  }
   
  .epgcell {
  color:#000000;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  float: left; 
  border-radius: 0px 0px 0px 0px; 
  border: 1px #333333;
  overflow: hidden; 
  position:relative; 
  height:36px; 
  margin-left:3px; 
  padding-top:2px;
  }
  
  .epgcell.odd{
  background-color: #aaaaaa; 
  }

  .epgcell.even{
  background-color: #888888; 
  }
  
  .epgcell.oddnow{
  background-color: #aaffaa; 
  }
  
  .epgcell.evennow{
  background-color: #88ff88;
  }
  
  .gesamt{
  width: 1100px;
  height: 779px;
  margin-left: 0px;
  padding: 0;
  }
  
  .info {
  display: none;
  position: fixed;
  z-index: 1;
  left: calc(50% - 300px);
  top: calc(50% - 200px);
  width: 600px;
  height: 400px;
  overflow: auto;
  background-color: #ffffff;
  background-color: rgba(255,255,255,0.95);
  border-radius: 20px 20px 20px 20px;
  }
  
  .closebutton {
  position: absolute;
  left: 450px;
  top: 350px;
  width: 150px;
  height: 50px;
  background-color: #ffffff;
  background-color: rgba(190,190,190,0.95);
  text-align: center;
  border-radius: 20px 0px 0px 0px;
  }
  
  .recordbutton {
  position: absolute;
  left: 0px;
  top: 350px;
  width: 150px;
  height: 50px;
  background-color: #ffffff;
  background-color: rgba(190,190,190,0.95);
  text-align: center;
  border-radius: 0px 20px 0px 0px;
  }
 
  ''')
def PrintDetailCSS():
    PrintHead('css')
    print('''  .EPGDetailTitle{
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  font-size:24px;
  font-wight:bold;
  }

  .EPGDetailContent{
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  }
  
  .record{
  color:#ff0000;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  }
  '''
  )
def PrintNowLine(CList):
    offsetpx=(((offset/-1)/scale)+55)
    heightpx=(40*len(CList)+20)
    return('<div class="nowline" style="height:%spx;left:%spx;"></div>'% (heightpx,offsetpx))
def PrintTimeLine(dtwd,servertype,scale):
    SecondsToFullHour=((60-int(dtwd.strftime("%M")))*60)+60-(int(dtwd.strftime("%S")))
    TimeLineString = "<thead height='20px' style='position:sticky; top:0px; z-index:50;'><tr><th class='pvrflavor'>"
    if (showflavor=='1'):
        TimeLineString += servertype
    TimeLineString += "</th><td style='background-Color:#333333;'><div style='height:20px;display: inline-flex;'>"
    if SecondsToFullHour > 2700:
        TimeLineString += ("<div style='width:%spx;' class=timeline20p></div>"%(((SecondsToFullHour-2700)//scale)-3))
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;15</font></div>"% (((3600/4)//scale)-1))  
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))         
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1)) 
    elif SecondsToFullHour > 1800:
        TimeLineString += ("<div style='width:%spx;' class=timeline20p></div>"%(((SecondsToFullHour-1800)//scale)-3))
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))  
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1)) 
    elif SecondsToFullHour > 900:
        TimeLineString += ("<div style='width:%spx;' class=timeline20p></div>"%(((SecondsToFullHour-900)//scale)-3))
        TimeLineString += ("<div class='timelinemarker10p'></div>")
        TimeLineString += ("<div style='width:%spx;' class=timeline10p><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1))  
    elif SecondsToFullHour >4*scale:
        TimeLineString += ("<div style='width:%spx;' class=timeline20p></div>"%(((SecondsToFullHour)//scale)-3))
    for x in range(1, 24):
        TimeLinePos=int(dtwd.strftime("%H")) + x
        if TimeLinePos > 23:
            TimeLinePos=TimeLinePos -24
        TimeLineString += ("<div class='timelinemarker20p'></div>")
        TimeLineString += ("<div style='width:%spx;' class='timeline20p'><font class=timecodehour>&nbsp;%s</font></div>"%((((3600/4)//scale)-1),TimeLinePos))
        TimeLineString += ("<div class=timelinemarker10p></div>")
        TimeLineString += ("<div style='width:%spx;' class='timeline10p'><font class=timecode>&nbsp;15</font></div>"% (((3600/4)//scale)-1))
        TimeLineString += ("<div class=timelinemarker10p></div>")
        TimeLineString += ("<div style='width:%spx;' class='timeline10p'><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))
        TimeLineString += ("<div class=timelinemarker10p></div>")
        TimeLineString += ("<div style='width:%spx;' class='timeline10p'><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1))
    TimeLineString += ("</div></td></tr></thead>")
    return TimeLineString
#NextPVR Functions
def DoAuthNPVR(server,pin):
    #Create Pin`s MD5 Hasch 
    pinmd5 = hashlib.md5(pin.encode('utf-8')).hexdigest()
    #Get Salt and SID from Nextpvr API
    try:
        webUrl  = urllib.request.urlopen('%s/service?method=session.initiate&ver=1.0&device=xbmc'%(server))    
        response = webUrl.read()
    except Exception as e:
        return '1'
    root = etree.fromstring(response)
    sid = root.find('sid').text
    salt = root.find('salt').text
    #Build Digest for login
    combinedMD5 = ":"
    combinedMD5 += pinmd5
    combinedMD5 += ":"
    combinedMD5 += salt
    accessmd5 = hashlib.md5(combinedMD5.encode('utf-8')).hexdigest()
    #Authenticate Session
    webUrl  = urllib.request.urlopen('%s/service?method=session.login&sid=%s&md5=%s'% (server,sid,accessmd5))
    Login= (webUrl.read()) 
    if('Login Failed' in str(Login)):
        return '0'
    else:
        return sid
def GetChannelListNPVR(server,SID):
    webUrl  = urllib.request.urlopen('%s/service?method=channel.list&extras=true&sid=%s'% (server,SID))
    root = etree.fromstring(webUrl.read())
    channell = root.find('channels')
    CList = [[]]
    for channel in list(channell):
        ChannelName = channel.find('name').text
        ChannelID = channel.find('id').text
        ChannelNumber = channel.find('number').text
        CList.append([ChannelName,ChannelID,ChannelNumber])
    return CList
def BuildEpgLineNPVR(server,Channel,SID,timenow,oddeven):
    webUrl  = urllib.request.urlopen('%s/service?method=channel.listings&channel_id=%s&genre=all&sid=%s&start=%s&end=%s'% (server,Channel,SID,timenow,timenow+86400))
    retval = "<td valign=top style='height:39px; width:1600px; white-Space:nowrap'><div class='epgrow'>"
    data = webUrl.read()
    root = etree.fromstring(data, parser=parser)
    listing = root.find('listings')
    for l in list(listing):
        if l.tag == "l":
            timestartabs = int(l.find('start').text[:-3])
            timestart = timestartabs-timenow
            timeend = (int(l.find('end').text[:-3]))-timenow
            dt = datetime.datetime.fromtimestamp(timestartabs)
            duration = (timeend-timestart)//60
            if timestart < 1:
                timestart=0
            if (timestart+offset) < 1:
                if oddeven == "even":
                    oddevenresult = "evennow"
                if oddeven == "odd":
                    oddevenresult = "oddnow"
            else:
                oddevenresult=oddeven
            retval += ('<div class="epgcell %s" style="width:'%(oddevenresult))
            retval += str(int((timeend-timestart)/scale)-3)
            if l.find('recording_id') is not None:
                retval += ('px;"><span class=epgtxt><a href="javascript:showinfodel(%s,%s)" width="320" height="320">'%(l.find('id').text,l.find('recording_id').text))
            else:
                retval += ('px;"><span class=epgtxt><a href="javascript:showinfo(%s)" width="320" height="320">'%(l.find('id').text))
            retval += l.find('name').text
            if l.find('recording_id') is not None:
                record="<font style='color:#ff0000;'>[REC]</font>"
            else:
                record=""
            minutes = dt.minute
            if minutes < 10:
                minutes = ("0%s"%(minutes))
            retval += ('</a></span><br><span class=epgtxt>%s ab %s:%s (%s Min)</span></div>'% (record,dt.hour, minutes,str(duration)))
    retval += "</div></td>"
    return retval
def PrintEPGNPVR(server,pin,scale):
    dtwd = datetime.datetime.now() + datetime.timedelta(seconds=offset)
    timenow=int(time.mktime(dtwd.timetuple()))
    PrintHead('html')
    sid = DoAuthNPVR(server,pin)
    if(sid == '0'):
        print('<html><head><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head><body><font color="#ff0000">login failed - wrong pin?</font><br>')
        if(enabledebug=='1'):
            print ('<a href=/cgi-bin/epg.py?page=debug>get debug infos</a>')
        else:
            print ('Enbale debuginfo with environmelnt variable enabledebug=1')
            print('</body></html>')
    elif(sid == '1'):
        print('<html><head><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head><body><font color="#ff0000">connection failed - wrong serveraddress?</font><br>')
        if(enabledebug=='1'):
            print ('<a href=/cgi-bin/epg.py?page=debug>get debug infos</a>')
        else:
            print ('Enbale debuginfo with environmelnt variable enabledebug=1')
            print('</body></html>')
    else:    
        CList=GetChannelListNPVR(server,sid)
        PrintHeader()
        print('<section class="gesamt">')
        print('<table>')
        if(showtimeline=='1'):
            print(PrintTimeLine(dtwd,'NextPVR',scale))
        for i in range(1,len(CList)):
            oddeven="odd"
            if i%2 == 0:
                oddeven="even"
            print('<tr><th class="chanellogo">')
            print('<img src="%s/service?method=channel.icon&channel_id=%s&sid=%s" style="height:30px;width=30px;" alt="%s">'% (server,CList[i][1],sid,CList[i][0]))
            print('</th>')
            print(BuildEpgLineNPVR(server,CList[i][1],sid,timenow,oddeven))
            print('</tr>')
        print('</table></section>')
        if(shownowline=='1'):
            print(PrintNowLine(CList))
        PrintFooter()  
def PrintEPGDetailNPVR(server,pin):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuthNPVR(server,pin)
    PrintHead('html')
    webUrl  = urllib.request.urlopen('%s/service?method=channel.listing&event_id=%s&sid=%s'% (server,eventid,sid))
    root = etree.fromstring(webUrl.read())
    event = root.find('event')
    Title = event.find('name').text
    Detail = event.find('description').text
    if event.find('recording_id') is not None:
        record="<span class='record'>[REC]</span>"
    else:
        record=""
    print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>%s</span><br><br><span class='EPGDetailContent'>%s</span>%s</body></html>"%(Title,Detail,record))
def PrintRecordEventNPVR(server,pin):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuthNPVR(server,pin)
    PrintHead('html')
    webUrl  = urllib.request.urlopen('%s/service?method=recording.save&event_id=%s&sid=%s'% (server,eventid,sid))
    result = webUrl.read()
    if "ok" in str(result):
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme geplant</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
def PrintRecordDeleteNPVR(server,pin):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuthNPVR(server,pin)
    PrintHead('html')
    webUrl  = urllib.request.urlopen('%s/service?method=recording.delete&recording_id=%s&sid=%s'% (server,eventid,sid))
    result = webUrl.read()
    if "ok" in str(result):
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme gelöscht</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
#TVHEADEND Functions
def GetChannelListTVH(server):
    webUrl  = urllib.request.urlopen('%s/api/channel/grid?sort=number'% (server))
    channell = json.loads(webUrl.read())
    CList = [[]]
    for channel in channell['entries']:
        ChannelName = channel['name']
        ChannelID = channel['uuid']
        ChannelNumber = channel['number']
        ChannelIcon = channel['icon_public_url']
        CList.append([ChannelName,ChannelID,ChannelNumber,ChannelIcon])
    return CList
def BuildEpgLineTVH(server,channeluuid,timenow,oddeven):
    webUrl  = urllib.request.urlopen('%s/api/epg/events/grid?channel=%s&limit=120'% (server,channeluuid))
    retval = "<td valign=top style='height:39px; width:1600px; white-Space:nowrap'><div class='epgrow'>"
    epglist = json.loads(webUrl.read())
    for epgentry in epglist['entries']:
        timestartabs = int(epgentry['start'])
        timestart = timestartabs-timenow
        timeend = int(epgentry['stop'])-timenow
        dt = datetime.datetime.fromtimestamp(timestartabs)
        duration = (timeend-timestart)//60
        if timestart < 1:
            timestart=0
        if (timestart+offset) < 1:
            if oddeven == "even":
                oddevenresult = "evennow"
            if oddeven == "odd":
                oddevenresult = "oddnow"
        else:
            oddevenresult=oddeven
        retval += ('<div class="epgcell %s" style="width:'%(oddevenresult))
        retval += str(int((timeend-timestart)/scale)-3)
        if 'dvrUuid' in epgentry:
            retval += ('px;"><span class=epgtxt><a href="javascript:showinfodel(%s,\'%s\')" width="320" height="320">'%(epgentry['eventId'],epgentry['dvrUuid']))
        else:
            retval += ('px;"><span class=epgtxt><a href="javascript:showinfo(%s)" width="320" height="320">'%(epgentry['eventId']))
        retval += epgentry['title']
        if 'dvrUuid' in epgentry:
            record="<font style='color:#ff0000;'>[REC]</font>"
        else:
            record=""
        minutes = dt.minute
        if minutes < 10:
            minutes = ("0%s"%(minutes))
        retval += ('</a></span><br><span class=epgtxt>%s ab %s:%s (%s Min)</span></div>'% (record,dt.hour, minutes,str(duration)))
    retval += "</div></td>"
    return retval
def PrintEPGTVH(server,scale):
    PrintHead('html')
    try:
        webUrl  = urllib.request.urlopen('%s/api/service/mapper/status'% (server))
        status = json.loads(webUrl.read())
    except Exception:
        print('<html><head><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head><body><font color="#ff0000">connection failed - wrong serveraddress?</font><br>')
        if(enabledebug=='1'):
            print ('<a href=/cgi-bin/epg.py?page=debug>get debug infos</a>')
        else:
            print ('Enbale debuginfo with environmelnt variable enabledebug=1')
        print('</body></html>')
        end()
    dtwd = datetime.datetime.now() + datetime.timedelta(seconds=offset)
    timenow=int(time.mktime(dtwd.timetuple()))
    CList=GetChannelListTVH(server)
    PrintHeader()
    print('<section class="gesamt">')
    print('<table>')
    if(showtimeline=='1'):
        print(PrintTimeLine(dtwd,'TVHeadend',scale))
    for i in range(1,len(CList)):
        oddeven="odd"
        if i%2 == 0:
            oddeven="even"
        print('<tr><th class="chanellogo">')
        print('<img src="%s/%s" style="height:30px;width=30px;" alt="%s">'% (server,CList[i][3],CList[i][1]))
        print('</th>')
        print(BuildEpgLineTVH(server,CList[i][1],timenow,oddeven))
        print('</tr>')
    print('</table></section>')
    if(shownowline=='1'):
        print(PrintNowLine(CList))
    PrintFooter()
def PrintEPGDetailTVH(server):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    PrintHead('html')
    webUrl  = urllib.request.urlopen('%s//api/epg/events/load?eventId=%s'% (server,eventid))
    epgdetail = json.loads(webUrl.read())
    for epgentry in epgdetail['entries']:
        Title = epgentry['title']
        Detail = epgentry['description']
    if 'dvrUuid' in epgentry:
        record="<span class='record'>[REC]</span>"
    else:
        record=""
    print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>%s</span><br><br><span class='EPGDetailContent'>%s</span>%s</body></html>"%(Title,Detail,record))
def PrintRecordEventTVH(server):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    PrintHead('html')
    #get recordprofile
    webUrl = urllib.request.urlopen('%s/api/dvr/config/grid'%(server))
    configdetail = json.loads(webUrl.read())    
    for configentry in configdetail['entries']:
        uuid = configentry['uuid']
        isactive = configentry['enabled']
        if(isactive):
            break
    webUrl1 = urllib.request.urlopen('%s/api/dvr/entry/create_by_event?event_id=%s&config_uuid=%s'% (server,eventid,uuid))
    recorddetail = json.loads(webUrl1.read())  
    if 'uuid' in recorddetail:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme geplant</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
def PrintRecordDeleteTVH(server):
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    PrintHead('html')
    webUrl = urllib.request.urlopen('%s/api/dvr/entry/cancel?uuid=%s'% (server,eventid))
    statuscode = webUrl.getcode()
    if (statuscode == 200):
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme gelöscht</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
#MythTV Functions
def GetChannelListMythTV(server):
    webUrl  = urllib.request.urlopen('%s/Channel/GetChannelInfoList?SourceID=0&StartIndex=1&OnlyVisible=false&Details=true'% (server))
    root = etree.fromstring(webUrl.read())
    channell = root.find('ChannelInfos')
    CList = [[]]
    for channel in list(channell):
        ChannelName = channel.find('ChannelName').text
        ChannelID = channel.find('ChanId').text
        ChannelNumber = channel.find('ChanNum').text
        ChannelIcon = channel.find('IconURL').text
        CList.append([ChannelName,ChannelID,ChannelNumber,ChannelIcon])
    return CList
def BuildEpgLineMythTV(server,channel,timenow,oddeven,videoserveroffsetseconds):
    dtstart = datetime.datetime.now() - datetime.timedelta(seconds=videoserveroffsetseconds) + datetime.timedelta(seconds=offset) 
    isostarttime = dtstart.isoformat('T','seconds')
    isostarttimewithz = isostarttime+'Z'
    dtend = dtstart + datetime.timedelta(seconds=86400)
    isoendtime = dtend.isoformat('T','seconds')
    isoendtimewithz = isoendtime+'Z'
    #read programm from guide service
    webUrl  = urllib.request.urlopen('%s/Guide/GetProgramList?StartTime=%s&EndTime=%s&ChanID=%s&details=false'% (server,isostarttimewithz,isoendtimewithz, channel))
    retval = "<td valign=top style='height:39px; width:1600px; white-Space:nowrap'><div class='epgrow'>"
    data = webUrl.read()
    root = etree.fromstring(data, parser=parser)
    listing = root.find('Programs')
    for l in list(listing):
        if l.tag == "Program":
            #handle the f*****g timeformat sql-iso-utc
            timestartdt = datetime.datetime.strptime(l.find('StartTime').text, '%Y-%m-%dT%H:%M:%SZ')
            timestartabs = int(time.mktime(timestartdt.timetuple())) + videoserveroffsetseconds
            timeenddt = datetime.datetime.strptime(l.find('EndTime').text, '%Y-%m-%dT%H:%M:%SZ')
            timeendabs = int(time.mktime(timeenddt.timetuple())) + videoserveroffsetseconds
            timestartshow =timestartdt + datetime.timedelta(seconds=videoserveroffsetseconds)            
            timestart = timestartabs-timenow
            duration = (timeendabs-timestartabs)//60
            if timestart < 1:
                timestart=0
            if (timestart+offset) < 1:
                if oddeven == "even":
                    oddevenresult = "evennow"
                if oddeven == "odd":
                    oddevenresult = "oddnow"
            else:
                oddevenresult=oddeven
            retval += ('<div class="epgcell %s" style="width:'%(oddevenresult))
            if (timestartabs < timenow):
                timestartabs=timenow
            retval += str(((timeendabs-timestartabs)//scale)-3)
            recording = l.find('Recording')
            channeldata = l.find('Channel')
            if (recording.find('Status').text=='WillRecord'):
                #retval += recording.find('RecordId').text
                #retval += ('%s/Guide/GetProgramList?StartTime=%s&EndTime=%s&ChanID=%s&details=false'% (server,isostarttimewithz,isoendtimewithz, channel))
                retval += ('px;"><span class=epgtxt><a href="javascript:showinfodelmythtv(\'%s\',\'%s\')" width="320" height="320">'%(channel, l.find('StartTime').text))
                record="<font style='color:#ff0000;'>[REC]</font>"
            else:
                retval += ('px;"><span class=epgtxt><a href="javascript:showinfomythtv(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" width="320" height="320">'% (channel, l.find('StartTime').text,l.find('EndTime').text,channeldata.find('CallSign').text,l.find('Title').text))
                record=""
            retval += l.find('Title').text
            minutes = timestartshow.minute
            if minutes < 10:
                minutes = ("0%s"%(minutes))
            retval += ('</a></span><br><span class=epgtxt>%s ab %s:%s (%s Min)</span></div>'% (record,timestartshow.hour, minutes,int(duration)))
    retval += "</div></td>"
    return retval
def PrintEPGMythTV(server,scale,offset):
    PrintHead('html')
    #check Server availability
    try:
        webUrl  = urllib.request.urlopen('%s/Myth/GetTimeZone'% (server))
        root = etree.fromstring(webUrl.read())
    except Exception:
        print('<html><head><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head><body><font color="#ff0000">connection failed - wrong serveraddress?</font><br>')
        if(enabledebug=='1'):
            print ('<a href=/cgi-bin/epg.py?page=debug>get debug infos</a>')
        else:
            print ('Enbale debuginfo with environmelnt variable enabledebug=1')
        print('</body></html>')
        end()
    #build fu****g timehandling with utc Dates in SQL format
    videoserveroffsetseconds = int(root.find('UTCOffset').text)
    dtwd = datetime.datetime.now() + datetime.timedelta(seconds=offset)
    timenow=int(time.mktime(dtwd.timetuple()))
    CList=GetChannelListMythTV(server)
    PrintHeader()
    print('<section class="gesamt">')
    print('<table>')
    if(showtimeline=='1'):
        print(PrintTimeLine(dtwd,'MythTV',scale))
    for i in range(1,len(CList)):
        oddeven="odd"
        if i%2 == 0:
            oddeven="even"
        print('<tr><th class="chanellogo">')
        print('<img src="%s%s&Height=25&Width=40" alt="%s">'% (server,CList[i][3],CList[i][0][:3]))
        print('</th>')
        print(BuildEpgLineMythTV(server,CList[i][1],timenow,oddeven,videoserveroffsetseconds))
        print('</tr>')
    print('</table></section>')
    if(shownowline=='1'):
        print(PrintNowLine(CList))
    PrintFooter()
def PrintEPGDetailMythTV(server):
    if "channel" in fs:
        channel = fs["channel"].value
    else:
        channel = "0"
    if "starttime" in fs:
        starttime = fs["starttime"].value
    else:
        starttime = "0"
    PrintHead('html')
    webUrl  = urllib.request.urlopen('%s/Guide/GetProgramDetails?StartTime=%s&ChanId=%s'% (server,starttime,channel))
    root = etree.fromstring(webUrl.read())
    title = root.find('Title').text
    detail = root.find('Description').text
    recording = root.find('Recording')
    record = recording.find('Status')
    if (recording.find('Status').text=='WillRecord'):
        record="<span class='record'>[REC]</span>"
    else:
        record=""
    print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>%s</span><br><br><span class='EPGDetailContent'>%s</span>%s</body></html>"%(title,detail,record))
def PrintRecordEventMythTV(server):
    if "starttime" in fs:
        starttime = fs["starttime"].value
    else:
        starttime = "0"
    if "endtime" in fs:
        endtime = fs["endtime"].value
    else:
        endtime = "0"
    if "channel" in fs:
        channel = fs["channel"].value
    else:
        channel = "0"
    if "callsign" in fs:
        callsign = fs["callsign"].value
    else:
        title = "0"
    if "title" in fs:
        title = fs["title"].value
    else:
        title = "0"
    PrintHead('html')
    data = {"Title":"","StartTime":"","EndTime":"","ChanId":"","Station":"","FindDay":"1","FindTime":"00:00:00","ParentId":"0","Type":"Single Record","SearchType":"Manual Search"}
    data['Title']=title
    data['StartTime']=starttime
    data['EndTime']=endtime
    data['Station']=callsign
    data['ChanId']=channel
    url_encoded_data = urllib.parse.urlencode(data)
    post_data = url_encoded_data.encode("utf-8")
    url=server+'/Dvr/AddRecordSchedule?%s'
    req = urllib.request.Request(url, post_data)
    webUrl = urllib.request.urlopen(req)
    data = webUrl.read()
    #b'<!--?xml version="1.0" encoding="UTF-8"?--><uint>34</uint>\n'
    if 'uint' in str(data):
        print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme geplant</span></body></html>")
    else:
        print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
def PrintRecordDeleteMythTV(server):
    if "starttime" in fs:
        starttime = fs["starttime"].value
    else:
        starttime = "0"
    if "channel" in fs:
        channel = fs["channel"].value
    else:
        channel = "0"
    PrintHead('html')
    data = {"StartTime":"","ChanId":""}
    data['StartTime']=starttime
    data['ChanId']=channel
    url_encoded_data = urllib.parse.urlencode(data)
    post_data = url_encoded_data.encode("utf-8")
    url=server+'/Dvr/GetRecordSchedule?%s'
    req = urllib.request.Request(url, post_data)
    webUrl = urllib.request.urlopen(req)
    root = etree.fromstring(webUrl.read())
    scheduleid = root.find('Id').text
    data = {"RecordId":""}
    data['RecordId']=scheduleid
    url_encoded_data = urllib.parse.urlencode(data)
    post_data = url_encoded_data.encode("utf-8")
    url=server+'/Dvr/RemoveRecordSchedule?%s'
    req = urllib.request.Request(url, post_data)
    webUrl = urllib.request.urlopen(req)
    data = webUrl.read()
    if 'true' in str(data):
        print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Planung gel&ouml;scht</span></body></html>")
    else:
        print("<!DOCTYPE html><html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
#Debug Infos
def PrintDebugNPVR(server,pin):
    PrintHead('html')
    print("<html><head><style>td{font-family: Arial, Helvetica, sans-serif;}</style></head><body><table>")
    print("<tr><td><b>environmentvariable</b></td><td><b>value</b></td></tr>")
    print("<tr><td>server</td><td>"+server+"</td></tr>")
    print("<tr><td>servertype</td><td>"+str(servertype)+"</td></tr>")
    print("<tr><td>pin</td><td>"+pin+"</td></tr>")
    print("<tr><td>scale</td><td>"+str(scale)+"</td></tr>")
    print("<tr><td>shownowline</td><td>"+str(shownowline)+"</td></tr>")
    print("<tr><td>showtimeline</td><td>"+str(showtimeline)+"</td></tr>")    
    print("<tr><td>enabledebug</td><td>"+str(enabledebug)+"</td></tr>")
    dtwd=datetime.datetime.now() + datetime.timedelta(seconds=0)
    print("<tr><td><b>systemvariable</b></td><td><b>value</b></td></tr>")
    print("<tr><td>Servertime</td><td>"+str(dtwd)+"</td></tr>")
    print("<tr><td>secs to full hour</td><td>"+str(((60-int(dtwd.strftime("%M")))*60)-(int(dtwd.strftime("%S"))))+"</td></tr>")  
    print("<tr><td><b>serverconnection</b></td><td><b>result</b></td></tr>")
    sid = DoAuthNPVR(server,pin)
    if(sid == '1'):
        print("<tr><td>connection</td><td>failed</td></tr>")
    else:
        print("<tr><td>connection</td><td>successful</td></tr>")
    if(sid == '0'):
        print("<tr><td>login</td><td>failed</td></tr>")
    else:
        print("<tr><td>login</td><td>successful</td></tr>")
    print("<tr><td>sessionId</td><td>"+sid+"</td></tr>")
    CList = GetChannelListNPVR(server,sid)
    print("<tr><td>channels</td><td>")
    for i in range(1,len(CList)):
        print(str(CList[i][0])+"; ")
    print("</td></tr>")    
    print("</table></body></html>")
def PrintDebugTVH(server):
    PrintHead('html')
    print("<html><head><style>td{font-family: Arial, Helvetica, sans-serif;}</style></head><body><table>")
    print("<tr><td><b>environmentvariable</b></td><td><b>value</b></td></tr>")
    print("<tr><td>server</td><td>"+server+"</td></tr>")
    print("<tr><td>servertype</td><td>"+str(servertype)+"</td></tr>")
    print("<tr><td>scale</td><td>"+str(scale)+"</td></tr>")
    print("<tr><td>shownowline</td><td>"+str(shownowline)+"</td></tr>")
    print("<tr><td>showtimeline</td><td>"+str(showtimeline)+"</td></tr>")    
    print("<tr><td>enabledebug</td><td>"+str(enabledebug)+"</td></tr>")
    dtwd=datetime.datetime.now() + datetime.timedelta(seconds=0)
    print("<tr><td><b>systemvariable</b></td><td><b>value</b></td></tr>")
    print("<tr><td>Servertime</td><td>"+str(dtwd)+"</td></tr>")
    print("<tr><td>secs to full hour</td><td>"+str(((60-int(dtwd.strftime("%M")))*60)-(int(dtwd.strftime("%S"))))+"</td></tr>")  
    print("<tr><td><b>serverconnection</b></td><td><b>result</b></td></tr>")
    try:
        webUrl  = urllib.request.urlopen('%s/api/service/mapper/status'% (server))
        status = json.loads(webUrl.read())
    except Exception:
        print("<tr><td>connection</td><td>failed</td></tr>")
        print("</table></body></html>")
        end()
    print("<tr><td>connection</td><td>successful</td></tr>")
    CList = GetChannelListTVH(server)
    print("<tr><td>channels</td><td>")
    for i in range(1,len(CList)):
        print(str(CList[i][0])+"; ")
    print("</td></tr>")    
    print("</table></body></html>") 
def PrintDebugMythTV(server):
    #PrintEPGMythTV(server)
    PrintHead('html')
    print("server "+server+"<br>")
    print("scale "+str(scale)+"<br>")
    print("servertype "+str(servertype)+"<br>")
    dtwd=datetime.datetime.now() + datetime.timedelta(seconds=0)
    print("Servertime"+str(dtwd)+"<br>")
    print("secstofullhour"+str(((60-int(dtwd.strftime("%M")))*60)-(int(dtwd.strftime("%S"))))+"<br>")  

    #print(GetChannelListMythTV(server))

#Main
fs = cgi.FieldStorage()
if "page" in fs:
    page = fs["page"].value
else:
    page=""

if (stype == 0):
    if page == "epg":
        PrintEPGNPVR(server,pin,scale)
    elif page == "epgcss":
        PrintEPGCSS()
    elif page == "detailcss":
        PrintDetailCSS()
    elif page == "epg_detail":
        PrintEPGDetailNPVR(server,pin) 
    elif page == "recordevent":
        PrintRecordEventNPVR(server,pin)
    elif page == "recorddelete":
        PrintRecordDeleteNPVR(server,pin)
    elif page == "debug":    
        if(enabledebug=='1'):
            PrintDebugNPVR(server,pin)
        else:
            PrintEPGNPVR(server,pin,scale)
    else:
        PrintEPGNPVR(server,pin,scale)
if (stype == 1):
    offset=0
    shownowline=0
    if page == "epg":
        PrintEPGTVH(server,scale)
    elif page == "epgcss":
        PrintEPGCSS()
    elif page == "detailcss":
        PrintDetailCSS()
    elif page == "epg_detail":
        PrintEPGDetailTVH(server) 
    elif page == "recordevent":
        PrintRecordEventTVH(server)
    elif page == "recorddelete":
        PrintRecordDeleteTVH(server)
    elif page == "debug":  
        if(enabledebug=='1'):
            PrintDebugTVH(server)
        else:
            PrintEPGTVH(server,scale)
    else:
        PrintEPGTVH(server,scale)
if (stype == 2):
    if page == "epg":
        PrintEPGMythTV(server,scale,offset)
    elif page == "epgcss":
        PrintEPGCSS()
    elif page == "detailcss":
        PrintDetailCSS()
    elif page == "epg_detail":
        PrintEPGDetailMythTV(server) 
    elif page == "recordevent":
        PrintRecordEventMythTV(server)
    elif page == "recorddelete":
        PrintRecordDeleteMythTV(server)
    elif page == "debug":  
        if(enabledebug=='1'):
            PrintDebugMythTV(server)
        else:
            PrintEPGMythTV(server,scale,offset)
    else:
        PrintEPGMythTV(server,scale,offset)