class RouterInformation:
    def __init__(self, name):
        self.name = name
        self.interfaces = []
        self.neighbours = []
        self.routes = []

    def get_ip(self):
        return self.interfaces[-1]

    def add_interfaces(self, name, ip, mask, velocity):
        self.interfaces.append(Interfaces(name, ip, mask, velocity))

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def get_neighbours(self):
        return self.neighbours

    def add_routes(self, networks, masks, nexthop, RType):
        for x, y, z, n in zip(networks, masks, nexthop, RType):
            RType = ''
            if n.value == '1':
                RType = 'Other'
            elif n.value == '2':
                RType = 'Reject'
            elif n.value == '3':
                RType = 'Local'
            elif n.value == '4':
                RType = 'Remote'
            route = Route(x.value, y.value, z.value, RType)
            self.routes.append(route)

    def print_router_information(self):
        print "     **********************"
        print "             " + self.name
        print "     **********************"
        print "# Interfaces"
        print "NAME             | IP    | MASK      | SPEED"
        self.print_interfaces()
        print "# Neighbours"
        for neighbour in self.neighbours:
            print "- " + str(neighbour)

    def print_routes(self):
        print "# Routes"
        print "NETWORK  | MASK    | NEXT HOP   | TYPE"
        for route in self.routes:
            print route.network, route.mask, route.nextHop, route.RType

    def print_interfaces(self):
        for interface in self.interfaces:
            print interface.name, interface.ip, interface.mask, \
                interface.velocity, "Mbps"


class Topology:
    def __init__(self):
        self.routers = []
        self.name = []

    def get_list(self):
        return self.routers

    def get_names(self):
        return self.name

    def add_router(self, item, name):
        self.routers.append(item)
        self.name.append(name)


class Interfaces:
    def __init__(self, name, ip, mask, velocity):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.velocity = velocity


class Route:
    def __init__(self, network, mask, nexthop, RType):
        self.network = network
        self.mask = mask
        self.nextHop = nexthop
        self.RType = RType
