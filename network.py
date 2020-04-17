from platform import system, release

from netifaces import interfaces, ifaddresses, AF_LINK, AF_INET, AF_INET6
from netifaces import gateways

from netaddr import IPNetwork, IPAddress

from uuid import getnode


class MyInfo:
    def __init__(self):
        self.os = self.get_os()
        self.network_interface = self.get_network_interface_list()
        self.mac = self.get_mac_address()
        self.ip = self.get_ip_address()

        self.subnetmask = self.get_subnetmask()
        self.prefix = self.get_prefix()

        self.gateway_ip = self.get_gateway_info()[0]
        self.gateway_network_interface = self.get_gateway_info()[1]
        

    def get_os(self):
        return system() + ' ' + release()


    def get_network_interface_list(self):
        # 여러개 일 경우도 해야될 듯
        # lo 없애는거 해야될 듯
        return interfaces()[1]

    
    def get_gateway_info(self):
        default = gateways()['default']

        return default[2]

    
    # def get_mac_address(self):
    #     interface_name = self.get_network_interface()
    #     return str(ifaddresses(interface_name)[AF_LINK][0]['addr'])
    def get_mac_address(self):
        mac = ':'.join(("%012X" % getnode())[i : i + 2] for i in range(0, 12, 2))
        return mac

    
    def get_ip_address(self):
        return str(ifaddresses(self.network_interface)[AF_INET][0]['addr'])

    
    def get_subnetmask(self):
        return str(ifaddresses(self.network_interface)[AF_INET][0]['netmask'])


    def get_prefix(self):
        netmask = self.subnetmask

        ip = IPNetwork(self.ip + '/' + netmask)
        
        return str(ip[0]) + '/' + str(IPAddress(netmask).netmask_bits())


    def get_ip_by_index(self, index=1):
        network: IPNetwork = IPNetwork(self.get_prefix())
        return str(network[index])