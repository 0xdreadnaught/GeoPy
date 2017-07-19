import sys
from pygeoip import GeoIP

#load IP location database to variable
geo = GeoIP('GeoLiteCity.dat')

#grab IP address from cli arg
ip = sys.argv[1]

ipInfo = geo.record_by_addr(ip)
print "Target: " + ip
print "Country: " + ipInfo['country_name']
print "Region: " + ipInfo['city'] + ", " + ipInfo['region_code']
print "GPS: " + str(ipInfo['latitude']),",",str(ipInfo['longitude'])

