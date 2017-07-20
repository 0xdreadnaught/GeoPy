import sys
import urllib2
import html2text
import socket
from pygeoip import GeoIP

def getISP(ip):
	tracker = "http://www.ip-adress.com/ip_tracer/"
	header = {'User-Agent': 'Mozilla/5.0'}
	request = urllib2.Request(tracker + ip, headers=header)
	data = urllib2.urlopen(request).read()
	html = html2text.HTML2Text()
	html.ignore_links = True
	info = html.handle(data)
	cleanInfo = info.encode('ascii', 'ignore').decode('ascii')
	
	lines = cleanInfo.splitlines()
	for line in lines:
		if ("Organization| " in line):
			org = line


	if(len(org) > 0):
		print "\033[1;32;40m Organization:\033[0;37;40m " + org[14:] + "\n" 
	else:
		print "\033[1;32;40m Organization:\033[0;37;40m Uknown\n"

def skipIP(ip):
	print "\033[0;31;40m Skipping: " + "\033[0;37;40m" + ip.strip() + "\n"

def printInfo(ip, info):
	print "\033[1;32;40m Target: " + "\033[0;37;40m" + str(ip).strip()
        print "\033[1;32;40m Country: " + "\033[0;37;40m" + str(info['country_name'])
        print "\033[1;32;40m Region: " + "\033[0;37;40m" + str(info['city']) + ", " + str(info['region_code'])
        print "\033[1;32;40m GPS: " + "\033[0;37;40m" + str(info['latitude']) + ", " + str(info['longitude'])
	
	getISP(ip)

def main():
	#load IP location database to variable
	geo = GeoIP('GeoLiteCity.dat')
	
	#get mode arg
	mode = sys.argv[1]
	
	#get ip for normal mode
	ip = sys.argv[2]

	if(mode == "-n"):
		ipInfo = geo.record_by_addr(ip)
		#now we need to check the first octet of the address to skip over local IPs
		#first we'll handle
		if(ip.startswith("10."))  or (ip.startswith("192.")) or (ip.startswith("172.")) or (ip.startswith("127.") or (ip.startswith("0."))):
			skipIP(ip)
		elif("." not in ip[:3]):
			num = int(ip[:3])
			if(num > 223):			
				skipIP(ip)
			else:
				printInfo(ip, ipInfo)
		else:
			printInfo(ip, ipInfo)
	
	elif(mode == "-l"):
		ips = sys.argv[2]
		ipList = open(ips)
		
		for IP in ipList.readlines():
			ipInfo = geo.record_by_addr(IP)
			#now we need to check the first octet of the address to skip over local IPs
			#first we'll handle
			if(IP.startswith("10."))  or (IP.startswith("192.")) or (IP.startswith("172.")) or (IP.startswith("127.") or (IP.startswith("0."))):
				skipIP(IP)
			elif("." not in IP[:3]):
	                        num = int(IP[:3])
     		                if(num > 223):
                	                skipIP(IP)
				else:
					printInfo(IP, ipInfo)
			else:
				printInfo(IP, ipInfo)
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
			if(IP.startswith("10."))  or (IP.startswith("192.")) or (IP.startswith("172.")) or (IP.startswith("127.") or (IP.startswith("0."))):
				pass
			elif("." not in IP[:3]):
	                        num = int(IP[:3])
        	                if(num > 223):
                	                pass
				else:
					printInfo(IP, ipInfo)
			else:
                        	printInfo(IP, ipInfo)			
	else:
		print "Something went wrong"
		
main()
