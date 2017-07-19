# GeoPy
Python based IP geolocation
Uses the pygeoip library and GeoLiteCity database to id info about IP addresses
Currently returns IP, Country, City, Region, and lat/long data

usage: 

	single target
	geopy.py -n <ipaddress>

	list mode
	geopy.py -l <file>    

	pcap mode
	geopy.py -p <file>

Some countries will thrown exceptions for city and region, so they will respond with "none". Cayman Islands would be an example where city and region are "none". 
Pcap mode ignores local IP address, 0.0.0.0, and anthing above 223 as they are all reserved for things like multicast
