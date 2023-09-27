import sys
from scapy.all import *

print(conf.ifaces)

while True:
    sniff(iface="Software Loopback Interface 1", prn = lambda x:x.show())