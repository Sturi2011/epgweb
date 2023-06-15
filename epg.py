#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#'''
# Custom Web EPG Server for Nextpvr
#
# Copyright (c) 2023 Andreas Fohl <andreas@fohl.net>
# Under GPL V3 License (http://www.opensource.org/licenses/mit-license.php)
#
# https://github.com/sturi2011/nextpvrepg
#'''
import cgi
import urllib.request
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
config = configparser.ConfigParser()
config.sections()
config.read('epg.conf')
sid=""
pin=config['EPG']['pin']
server=config['EPG']['server']
scale=int(config['EPG']['scale'])



def PrintCSSHead():
    print('''Content-Type: text/css; charset=utf-8\n''')
def PrintHTMLHead():
    print('''Content-Type: text/html; charset=utf-8\n''')
def PrintHeader():
    print('''<html>
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
        function record(elementId) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recordevent&eventId=" + elementId + "' width='100%'></object>"
            var rbutton = document.getElementById("recordbutton")
            rbutton.style.display = "none";
        }
        function recorddel(elementId) {
            document.getElementById("recorddetail").innerHTML="<object type='text/html' data='/cgi-bin/epg.py?page=recorddelete&eventId=" + elementId + "' width='100%'></object>"
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
    print('<!--')
    print(pin)
    print(server)
    print(scale)
    print('-->')
    print('''</body>
</html>''')
def PrintEPGCSS():
    PrintCSSHead()
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
  font-size:10;
  color:#ffffff;
  font-family: "Helvetica Neue", "Helvetica", "Open Sans", "Arial", sans-serif;
  valign:top;
  }
  
  .timecodehour{
  font-size:14;
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
  
  .timeline {
  background-color: #333333;
  }
  
  .epgtext {
  color: #ffffff;
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
    PrintCSSHead()
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
def DoAuth(PIN):
    #Create MD5 Hasch of Pin
    pinmd5 = hashlib.md5("0000".encode('utf-8')).hexdigest()
    #Get Salt and SID from Nextpvr API
    webUrl  = urllib.request.urlopen('%s/service?method=session.initiate&ver=1.0&device=xbmc'%(server))
    root = etree.fromstring(webUrl.read())
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
    Login= (webUrl.read()) #Have to check if rsp=ok mayby later
    return sid
def GetChannelList(SID):
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
def BuildEpgLine(Channel,SID,timenow,oddeven):
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
                if oddeven == "even":
                    oddevenresult = "evennow"
                if oddeven == "odd":
                    oddevenresult = "oddnow"
            else:
                oddevenresult=oddeven
            retval += ('<div class="epgcell %s" style="width:'%(oddevenresult))
            retval += str(((timeend//scale)-(timestart//scale))-3)
            if l.find('recording_id') is not None:
                retval += (';"><span class=epgtxt><a href="javascript:showinfodel(%s,%s)" width="320" height="320">'%(l.find('id').text,l.find('recording_id').text))
            else:
                retval += (';"><span class=epgtxt><a href="javascript:showinfo(%s)" width="320" height="320">'%(l.find('id').text))
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
def PrintEPG():
    gmt = time.gmtime()
    timenow = calendar.timegm(gmt)
    timenow = timenow + 0
    sid = DoAuth(pin)
    CList=GetChannelList(sid)
    PrintHTMLHead()
    PrintHeader()
    print('<section class="gesamt">')
    print('<table>')
    print('<thead height="20px" style="position:sticky; top:0px; z-index:100;"><tr><th class="chanellogo"></th><td style="background-Color:#333333;">')
    PrintTimeLine()
    print('</td></tr></thead>')
    for i in range(1,len(CList)):
        oddeven="odd"
        if i%2 == 0:
            oddeven="even"
        print('<tr><th class="chanellogo">')
        print('<a href="%s/live?channel=%s&sid=%s"><img src="%s/service?method=channel.icon&channel_id=%s&sid=%s" style="height:30;width=30;" alt="%s">'% (server,CList[i][2],sid,server,CList[i][1],sid,CList[i][0]))
        print('</th>')
        print(BuildEpgLine(CList[i][1],sid,timenow,oddeven))
        print('</tr>')
    print('</table></section>') 
    PrintFooter()    
def PrintEPGDetail():
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuth(pin)
    PrintHTMLHead()
    webUrl  = urllib.request.urlopen('%s/service?method=channel.listing&event_id=%s&sid=%s'% (server,eventid,sid))
    root = etree.fromstring(webUrl.read())
    event = root.find('event')
    Title = event.find('name').text
    Detail = event.find('description').text
    if event.find('recording_id') is not None:
        record="<span class='record'>[REC]</span>"
    else:
        record=""
    print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>%s</span><br><br><span class='EPGDetailContent'>%s</span>%s</body></html>"%(Title,Detail,record))
def PrintRecordEvent():
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuth(pin)
    PrintHTMLHead()
    webUrl  = urllib.request.urlopen('%s/service?method=recording.save&event_id=%s&sid=%s'% (server,eventid,sid))
    result = webUrl.read()
    if "ok" in str(result):
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme geplant</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
def PrintRecordDelete():
    if "eventId" in fs:
        eventid = fs["eventId"].value
    else:
        eventid = "0"
    sid = DoAuth(pin)
    PrintHTMLHead()
    webUrl  = urllib.request.urlopen('%s/service?method=recording.delete&recording_id=%s&sid=%s'% (server,eventid,sid))
    result = webUrl.read()
    if "ok" in str(result):
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Aufnahme gelöscht</span></body></html>")
    else:
        print("<html><head><link rel='stylesheet' href='/cgi-bin/epg.py?page=detailcss'></head><body><br><span class='EPGDetailTitle'>Fehlgeschlagen</span></body></html>")
def PrintTimeLine():
    gmt = time.localtime()
    SecondsToFullHour=((60-gmt.tm_min)*60)+(60-gmt.tm_sec)
    TimeLineString = "<div style='height:20px;display: inline-flex;'>"
    if SecondsToFullHour > 2700:
        TimeLineString += ("<div style='width:%s; height:20px;position: relative;' class=timeline></div>"%(((SecondsToFullHour-2700)//scale)-3))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;15</font></div>"% (((3600/4)//scale)-1))  
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))         
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1)) 
    elif SecondsToFullHour > 1800:
        TimeLineString += ("<div style='width:%s; height:20px;position: relative;' class=timeline></div>"%(((SecondsToFullHour-1800)//scale)-3))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))  
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1)) 
    elif SecondsToFullHour > 900:
        TimeLineString += ("<div style='width:%s; height:20px;position: relative;' class=timeline></div>"%(((SecondsToFullHour-900)//scale)-3))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1))  
    elif SecondsToFullHour >4*scale:
        TimeLineString += ("<div style='width:%s; height:20px;position: relative;' class=timeline></div>"%(((SecondsToFullHour)//scale)-3))
    for x in range(1, 24):
        TimeLinePos=gmt.tm_hour + x
        if TimeLinePos > 23:
            TimeLinePos=TimeLinePos -24
        TimeLineString += ("<div style='width:1px; height:20px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:20px;position: relative;' class=timeline><font class=timecodehour>&nbsp;%s</font></div>"%((((3600/4)//scale)-1),TimeLinePos))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;15</font></div>"% (((3600/4)//scale)-1))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;30</font></div>"% (((3600/4)//scale)-1))
        TimeLineString += ("<div style='width:1px; height:10px;position: relative; background-Color:#ffffff;'></div>")
        TimeLineString += ("<div style='width:%spx; height:10px;position: relative;' class=timeline><font class=timecode>&nbsp;45</font></div>"% (((3600/4)//scale)-1))
    TimeLineString += ("</div>")
    print(TimeLineString)

#Main
fs = cgi.FieldStorage()
if "page" in fs:
    page = fs["page"].value
else:
    page=""
    
if page == "epg":
    PrintEPG()
elif page == "epgcss":
    PrintEPGCSS()
elif page == "detailcss":
    PrintDetailCSS()
elif page == "epg_detail":
    PrintEPGDetail()    
elif page == "recordevent":
    PrintRecordEvent()
elif page == "recorddelete":
    PrintRecordDelete()
elif page == "debug":    
    sid = DoAuth(pin)
    PrintHTMLHead()
else:
    PrintEPG()
