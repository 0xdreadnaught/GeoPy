from pygeoip import GeoIP

geo = GeoIP('GeoLiteCity.dat')

ipInfo = geo.record_by_addr('72.14.199.81')
print ipInfo['country_name']
print ipInfo['latitude'],",",ipInfo['longitude']

