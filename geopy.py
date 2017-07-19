import sys
import dpkt
import socket
from pygeoip import GeoIP

#load IP location database to variable
geo = GeoIP('GeoLiteCity.dat')

#get mode arg
mode = sys.argv[1]

#get ip for normal mode
ip = sys.argv[2]

if(mode == "-n"):
	ipInfo = geo.record_by_addr(ip)
	print "Target: " + ip
	print "Country: " + str(ipInfo['country_name'])
	print "Region: " + str(ipInfo['city']) + ", " + str(ipInfo['region_code'])
	print "GPS: " + str(ipInfo['latitude']),",",str(ipInfo['longitude'])
elif(mode == "-l"):
	ips = sys.argv[2]
	ipList = open(ips)
	
	for IP in ipList.readlines():
		ipInfo = geo.record_by_addr(IP)
		print "Target: " + str(IP).strip()
		print "Country: " + str(ipInfo['country_name'])
		print "Region: " + str(ipInfo['city']) + ", " + str(ipInfo['region_code'])
		print "GPS: " + str(ipInfo['latitude']) + ", " + str(ipInfo['longitude'])
		print ""
elif(mode == "-p"):
	pcap = sys.argv[2]
	pcapdump = open(pcap, 'rb')
	pcapReader = dpkt.pcap.Reader(pcapdump)

	iplist = []
	
	for time,frame in pcapReader:
		eth = dpkt.ethernet.Ethernet(frame)
		if(eth.type != dpkt.ethernet.ETH_TYPE_IP): continue
		ip = eth.data		
		src = socket.inet_ntoa(ip.src)
		dst = socket.inet_ntoa(ip.dst)
		if not(src in iplist):
			iplist.append(src)
		if not(dst in iplist):
			iplist.append(dst)

	for IP in iplist:				
		ipInfo = geo.record_by_addr(IP)
		
		#now we need to check the first octet of the address to skip over local IPs
		#first we'll handle 
		if(IP.startswith("10."))  or (IP.startswith("192.")) or (IP.startswith("172.")) or (IP.startswith("127.")):
	                #do nothing
			pass
		elif("." not in IP[:3]):
			if(IP > 223):
				pass
		elif(IP == "0.0.0.0"):
			pass
		else:
			print "Target: " + str(IP).strip()
			print "Country: " + str(ipInfo['country_name'])
			print "Region: " + str(ipInfo['city']) + ", " + str(ipInfo['region_code'])
			print "GPS: " + str(ipInfo['latitude']) + ", " + str(ipInfo['longitude'])
	                print ""
			
else:
	print "Something went wrong"
