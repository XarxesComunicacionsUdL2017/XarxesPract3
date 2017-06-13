import os
from easysnmp import Session
import strings
import optparse
from utils import RouterInformation, Topology
__version__ = 1.0
__authors__ = "Nil Agut Marin i Jaume Giralt Barbe"


def connect(hostname, community):
    return Session(hostname=hostname, version=2, community=community)


def get_host_name(session):
    return session.get(strings.RouterName).value


def get_interface_information(session, interface):
    index = (session.get(strings.index + interface.value))
    name = (session.get(strings.name + index.value))
    mask = (session.get(strings.mask + interface.value))
    speed = int((session.get(strings.speed + index.value)).value) / 1000000
    return name.value, interface.value, mask.value, speed


def analyze_router(topology, ip):
    interfaces = []
    neighbours = []
    session = connect(ip, options.community)
    router = RouterInformation(get_host_name(session))
    topology.add_router(router, get_host_name(session))
    for interface in session.walk(strings.Interface):
        name, network, mask, speed = \
            get_interface_information(session, interface)
        router.add_interfaces(name, network, mask, speed)
    for neighbour in session.walk(strings.Neighbour):
        actual = get_host_name(connect(neighbour.value, options.community))
        router.add_neighbour(actual)
        neighbours.append(neighbour.value)
    return interfaces, neighbours


def analyze_topology(ip):
    topology = Topology()
    stack = [ip]
    while len(stack) > 0:
        network = stack.pop()
        if get_host_name(connect(network, options.community)) not \
                in topology.name:
            interfaces, neighbours = analyze_router(topology, network)
            for x in neighbours:
                stack.append(x)
    return topology.get_list()


def analyze_routes(router):
    session = connect(router.get_ip().ip, options.community)
    networks = session.walk(strings.network)
    masks = session.walk(strings.RMask)
    nexthop = session.walk(strings.nextHop)
    RType = session.walk(strings.Rtype)
    router.add_routes(networks, masks, nexthop, RType)


def validate(router, x, temporal):
    return str(router.name)+str(x) in temporal or str(x)+str(router.name) \
                                                  in temporal


def write_script(routers):
    outfile = open('data.dot', 'w')
    outfile.write(strings.HeadFile)
    temporal = []
    for router in routers:
        for x in router.get_neighbours():
            if not validate(router, x, temporal):
                outfile.write(str(router.name) + ' -- ' + str(x) + ';' + '\n')
                temporal.append(str(router.name)+str(x))
                temporal.append(str(x)+str(router.name))
    outfile.write("}")
    outfile.close()


def graph_creator(routers):
    write_script(routers)
    os.system('dot data.dot -o grafo1.png -Tpng -Grankdir=LR')
    print "Graph created"
    #os.system('rm data.dot')


def main():
    routers = analyze_topology(options.ip)
    for router in routers:
        analyze_routes(router)
        router.print_router_information()
        router.print_routes()
    graph_creator(routers)


if __name__ == '__main__':
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
                                   version=__version__)
    parser.add_option("-i", "--ip", action="store", type="string",
                      dest="ip", help="write ip of the host", metavar="IP")
    parser.add_option("-c", "--community", action="store", type="string",
                      dest="community",
                      help="write the community", metavar="COMMUNITY")
    (options, args) = parser.parse_args()
    if not options.ip:
        parser.error("The ip was not provided")
    if not options.community:
        parser.error("The community was not provided")
    main()
