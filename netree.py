from base import Base
from network import MyInfo
from arp import ArpScan
from packet import ArpPacket

from prettytable import PrettyTable


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

    pretty_table = PrettyTable(['IP Address', 'MAC Address'])
        
    for result in results:
        pretty_table.add_row([result['ip-address'], result['mac-address']])


    print(pretty_table)