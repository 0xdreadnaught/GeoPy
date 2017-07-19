import sys
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
else:
	print "Something went wrong"
