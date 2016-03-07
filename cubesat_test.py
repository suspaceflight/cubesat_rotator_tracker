# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:19:48 2016

@author: BEE
""Gives the azimuth and elvation angles every two seconds for the cubesat given
 cubesat name, and number x=1, connects to server """
import socket
import time
import datetime
import urllib2
from pyorbital import tlefile
from pyorbital import orbital
def cubesat_t(cubesat,x):   
     TCP_IP = '127.0.0.1'
     TCP_PORT = 5005
     BUFFER_SIZE = 1024
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     if x==1:
         s.connect((TCP_IP, TCP_PORT))
     response = urllib2.urlopen('http://celestrak.com/NORAD/elements/cubesat.txt')
     html = response.read()
     f = open('tle1.txt', 'r+')
     f.write(html)
     f.close()  
     tle=tlefile.read(cubesat,'tle1.txt')
     inc = tle.inclination
     print(inc)
     lon,lat = -1.394,50.9354
     alt=41
     utc_time = datetime.datetime.utcnow()
     
     passhrs=20
     o=orbital.Orbital('tisat 1','tle1.txt')
     print(o)
     p=o.get_next_passes(utc_time,passhrs,lon,lat,alt)
     print(p) 
     for i in range(0,len(p)):
         d1=o.get_observer_look(p[i][0], lon, lat, alt)
         d2=o.get_observer_look(p[i][1], lon, lat, alt)
         d3=o.get_observer_look(p[i][2], lon, lat, alt)
         print(i+1)         
         print 'start time:', p[i][0]
         print'AOS azimuth, elevation:' ,d1[0],d1[1]
         print'maximum elevation time:', p[i][2]
         print'Max azimuth, elevation:' ,d3[0],d3[1]
         print'end time:', p[i][1]
         print'LOS azimuth, elevation:' ,d2[0],d2[1]
     ip=0
     t=[1]
     for i in range(len(t)):
         l=p[i][0]
         dt=2
         if l.minute!=0 and l.minute!=1:
             utctime2=datetime.datetime(l.year,l.month,l.day,l.hour,l.minute-2,l.second)
         else:
             utctime2=datetime.datetime(l.year,l.month,l.day,l.hour-1,59,l.second) 
         if (utctime2.second%2==0) :
             utctime1=utctime2
         else:
            utctime2=datetime.datetime(l.year,l.month,l.day,l.hour-1,59,l.second-1)
            utctime1=utctime2
         while p[i][1]>=utctime1:
             if utctime1.second<58:
                 utctime1=datetime.datetime(utctime1.year,utctime1.month,utctime1.day,utctime1.hour,utctime1.minute,utctime1.second+dt) 
             elif utctime1.second==58:
                 if utctime1.minute<59:
                     utctime1=datetime.datetime(utctime1.year,utctime1.month,utctime1.day,utctime1.hour,utctime1.minute+1,0) 
                 elif utctime1.minute==59:
                     if utctime1.hour<23:
                         utctime1=datetime.datetime(utctime1.year,utctime1.month,utctime1.day,utctime1.hour+1,0,0) 
                     elif utctime1.hour==23:
                         if utctime1.month in [1,3,5,7,8,10,12] and utctime1.day<31:
                             utctime1=datetime.datetime(utctime1.year,utctime1.month,utctime1.day+1,0,0,0) 
                         elif utctime1.month in [1,3,5,7,8,10,12] and utctime1.day==31:
                             utctime1=datetime.datetime(utctime1.year,utctime1.month+1,1,0,0,0) 
                         elif utctime1.month in [4,6,9,11] and utctime1.month<30:
                             utctime1=datetime.datetime(utctime1.year,utctime1.day,utctime1.day+1,0,0,0) 
                         elif utctime1.month in [4,6,9,11] and utctime1.month==30:                             
                             utctime1=datetime.datetime(utctime1.year,utctime1.day+1,1,0,0,0)
             if p[i][0]<=utctime1:
                 look=o.get_observer_look(utctime1,lon,lat,alt)
                 "print look,utctime1"
                 angle=["%.3G" % (look[0]),"%.3G" % (look[1])]
                 msg1= str(angle[0])+','+str(angle[1])
                 if x==1:
                     s.send(msg1)
                 print msg1
                 time.sleep(2)
             ip=ip+1        
     return()
    