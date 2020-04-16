from base import Base
from network import MyInfo
from arp import ArpScan
from packet import ArpPacket


if __name__ == '__main__':
    base = Base()
    mine = MyInfo()
    arp = ArpScan()

    base.print_banner()

    interface = mine.get_network_interface_list()

    print('My Network Interface:  ', interface)

    print('My IP Address:         ', mine.get_ip_address(interface))
    print('My MAC Address:        ', mine.get_mac_address())

    print('Useable IP:            ', mine.get_ip_by_index(interface, 1),
                                  '~',
                                   mine.get_ip_by_index(interface, -2))


    results = arp.scan(interface, 
                       mine.get_mac_address(),
                       mine.get_ip_address(interface))