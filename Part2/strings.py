RouterName = 'SNMPv2-MIB::sysName.0'
Interface = 'RFC1213-MIB::ipAdEntAddr'
Neighbour = 'OSPF-MIB::ospfNbrIpAddr'

#Interface Description
index = 'RFC1213-MIB::ipAdEntIfIndex.'
name = 'IF-MIB::ifDescr.'
mask = 'RFC1213-MIB::ipAdEntNetMask.'
speed = 'IF-MIB::ifSpeed.'

#Network Description
network = 'IP-FORWARD-MIB::ipCidrRouteDest'
nextHop = 'IP-FORWARD-MIB::ipCidrRouteNextHop'
Rtype = 'IP-FORWARD-MIB::ipCidrRouteType'
RMask = 'IP-FORWARD-MIB::ipCidrRouteMask'

HeadFile = "graph A {"
