#!/usr/bin/python
##
#
# Created By:      Raj Geda
# Created on:      Mon Apr  6 16:52:05 2012 UTC
# Last Modified:   Fri oct  3 02:52:05 2015 UTC
#
# Revision Notes:
#
#-------------------------------------------------------------------------
#Description:
#
# https://%s/xmldata?item=CpqKey # to get KEY
# https://%s/xmldata?item=All # to get all data
# to get documentElements <>
#       node = data.documentElement
# to get documentElemnt TagName <RIMP>
#       TageName = node.nodeName
#       hsi = data.getElementsByTagName("HSI")
#
#-------------------------------------------------------------------------

import getopt
import sys
import socket
import string
import urllib2
from xml.dom import minidom

def usage():
        print "Usage: " + sys.argv[0] + " -h [hostname] or -i [ip addr] -p [nics, serial, mac0, mac1, uuid]"
        sys.exit(1)

ip = hostName = prt = None

optlist, args = getopt.getopt(sys.argv[1:], 'h:i:p:')
for k, v in optlist:
        if k == '-h':
                hostName = str(v)
        elif k == '-i':
                ip = str(v)
        elif k == '-p':
                prt = str(v).lower()
        else:
                usage()

#if serialNo == None:
        #usage()

if hostName:
        hostName = hostName
elif ip:
        hostName = ip
else:
        usage()

#print hostName.lower()
#print ip
ILO_URL = 'https://%s/xmldata?item=All'

def getdata(hostname):
        url = ILO_URL % hostname
        #print url
        req = urllib2.Request(url)
        xmldata = urllib2.urlopen(req)
        data = minidom.parse(xmldata)
        SBSN = data.getElementsByTagName("SBSN")[0].childNodes[0].data.strip()
        #if string.lower(SBSN).strip(' \t\n\r') == string.lower(serialNo).strip(' \t\n\r'):
        UUID = data.getElementsByTagName("cUUID")[0].childNodes[0].data
        NICS_RAW = data.getElementsByTagName("NICS")
        #print NICS
        if NICS_RAW:
          count=0
          NICS = {}
          for mac in NICS_RAW[0].getElementsByTagName('MACADDR'):
                NICS["MAC"+str(count)] = mac.childNodes[0].data
                count += 1
        #return dict(serial_no=SBSN,uuid=UUID,nic1=NIC1_MAC,nic2=NIC2_MAC)
        return dict(serial_no=SBSN,uuid=UUID,nics=NICS)

        #return "Error: SerialNumber does not Match. SerialNo from server("+SBSN.strip(' \t\n\r')+")"

if __name__ == "__main__":
        if not prt:
          print getdata(hostName)
        elif prt == 'nics':
          print getdata(hostName).get(prt)
        elif prt == 'nic1,serial':
          print getdata(hostName).get("nics")["MAC0"] + " " + getdata(hostName).get("serial_no")
        for count in range(0,len(getdata(hostName).get("nics"))):
           if prt == "nic"+str(count):
                print getdata(hostName).get("nics").get("MAC"+str(count))
