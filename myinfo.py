from platform import system, release

from netifaces import interfaces, ifaddresses, AF_LINK, AF_INET, AF_INET6
from netifaces import gateways

from netaddr import IPNetwork, IPAddress

from uuid import getnode

from prettytable import PrettyTable


class MyInfo:
    def __init__(self):
        self.os = self.get_os()
        self.network_interface = self.choose_network_interface()
        self.mac = self.get_mac_address()
        self.ip = self.get_ip_address()

        self.subnetmask = self.get_subnetmask()
        self.prefix = self.get_prefix()

        self.gateway_ip = self.get_gateway_info()[0]
        

    def get_os(self):
        return system() + ' ' + release()


    def choose_network_interface(self):
        lan_cards = interfaces()[1:]

        lan_card_table = PrettyTable(['Index', 'Lan Card', 'IP Address', 'MAC Address'])

        idxes = list()
        for idx, lan_card in enumerate(lan_cards):
            idxes.append(idx)

            try:
                ip = ifaddresses(lan_card)[AF_INET][0]['addr']
            except Exception as error:
                print(error)

            try:
                mac = ifaddresses(lan_card)[AF_LINK][0]['addr']
            except Exception as error:
                print(error)

            lan_card_table.add_row([idx, lan_card, ip, mac])

        print(lan_card_table)

        if len(lan_cards) == 1:
            return lan_cards[0]

        while True:
            try:
                choose_idx = int(input('Choose Index : '))
                
                if choose_idx in idxes:
                    break
            except Exception as error:
                print('INPUT NUMBER ( 0 ~ ', len(idxes)-1, ')')

        return lan_cards[choose_idx]

    
    def get_gateway_info(self):
        default = gateways()['default']

        return default[2]

    
    def get_mac_address(self):
        interface_name = self.network_interface
        return str(ifaddresses(interface_name)[AF_LINK][0]['addr'])

    
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