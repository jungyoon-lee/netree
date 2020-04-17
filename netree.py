from base import Base
from network import MyInfo
from arp import ArpScan
from packet import ArpPacket


if __name__ == '__main__':
    base = Base()
    myinfo = MyInfo()
    arp = ArpScan(myinfo)

    base.print_banner()

    print('My Network Interface: ', myinfo.network_interface)

    print('My IP Address:        ', myinfo.ip)
    print('My MAC Address:       ', myinfo.mac)

    print('Useable IP:           ', myinfo.get_ip_by_index(1),
                                 '~',
                                  myinfo.get_ip_by_index(-2))

    results = arp.scan()

    