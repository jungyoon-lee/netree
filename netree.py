from base import Base
from network import MyInfo
from packet import ArpPacket


if __name__ == '__main__':
    base = Base()
    mine = MyInfo()
    arp_scan = ArpPacket()

    base.print_banner()

    interface_name = mine.get_network_interface_list()

    print('My Network Interface:  ', interface_name)

    print('My IP Address:         ', mine.get_ip_address(interface_name))
    print('My MAC Address:        ', mine.get_mac_address())

    print('Useable IP:            ', mine.get_ip_by_index(interface_name, 1),
                                  '~',
                                   mine.get_ip_by_index(interface_name, -2))
    
    