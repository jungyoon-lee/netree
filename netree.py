from base import Base
from network import MyInfo
from arp import ArpScan
from packet import ArpPacket

from prettytable import PrettyTable


if __name__ == '__main__':
    base = Base()
    base.print_banner()
    
    myinfo = MyInfo()
    arp = ArpScan(myinfo)

    print('\nMy Network Interface      :', myinfo.network_interface)
    print('My IP Address             :', myinfo.ip)
    print('My MAC Address            :', myinfo.mac)

    print('\nGateway IP Address        :', myinfo.gateway_ip)

    print('Useable IP                :', myinfo.get_ip_by_index(2),
                                     '~',
                                     myinfo.get_ip_by_index(-2))


    # print('\nDNS Server IP Address     :', '0.0.0.0')

    results = arp.scan()

    result_table = PrettyTable(['IP Address', 'MAC Address', 'Product'])
        
    for result in results:
        result_table.add_row([result['ip-address'], result['mac-address'], result['product']])

    print(result_table)
