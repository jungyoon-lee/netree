from platform import system, release

from netifaces import interfaces, ifaddresses, AF_LINK, AF_INET, AF_INET6
from netifaces import gateways

from netaddr import IPNetwork, IPAddress

from uuid import getnode

class MyInfo:
    def get_os(self):
        return system() + ' ' + release()


    def get_network_interface_list(self):
        # 여러개 일 경우도 해야될 듯
        # lo 없애는거 해야될 듯
        return interfaces()[1]

    
    # def get_mac_address(self):
    #     interface_name = self.get_network_interface()
    #     return str(ifaddresses(interface_name)[AF_LINK][0]['addr'])
    def get_mac_address(self):
        mac = ':'.join(("%012X" % getnode())[i : i + 2] for i in range(0, 12, 2))
        return mac

    
    def get_ip_address(self, 
                       interface_name):
        return str(ifaddresses(interface_name)[AF_INET][0]['addr'])

    
    def get_subnetmask(self, 
                       interface_name):
        return str(ifaddresses(interface_name)[AF_INET][0]['netmask'])


    def get_prefix(self, 
                   interface_name):
        netmask = self.get_subnetmask(interface_name)
        ip_address = self.get_ip_address(interface_name)

        ip = IPNetwork(ip_address + '/' + netmask)
        
        return str(ip[0]) + '/' + str(IPAddress(netmask).netmask_bits())


    def get_ip_by_index(self, 
                        interface_name,
                        index=1):
        network: IPNetwork = IPNetwork(self.get_prefix(interface_name))
        return str(network[index])