from base import Base
from network import MyInfo
from arp import ArpScan
from icmp import IcmpScan

from prettytable import PrettyTable

from time import time


if __name__ == '__main__':
    base = Base()
    base.print_banner()
    
    myinfo = MyInfo()
    arp = ArpScan(myinfo)
    icmp = IcmpScan()

    print('\nMy Network Interface      :', myinfo.network_interface)
    print('My IP Address             :', myinfo.ip)
    print('My MAC Address            :', myinfo.mac)

    print('\nGateway IP Address        :', myinfo.gateway_ip)

    print('Useable IP                :', myinfo.get_ip_by_index(2),
                                     '~',
                                     myinfo.get_ip_by_index(-2))


    # print('\nDNS Server IP Address     :', '0.0.0.0')

    start_arp_scan = time()
    brothers = arp.scan()
    end_arp_scan = time()

    brother_table = PrettyTable(['IP Address', 'MAC Address', 'Product'])
        
    for brother in brothers:
        brother_table.add_row([brother['ip-address'], brother['mac-address'], brother['product']])

    print(brother_table)
    print(int(end_arp_scan - start_arp_scan), '초')
    
    grand_mother = icmp.scan_grandmother()

    results = icmp.scan_mother_brothers(grand_mother)
    
    print('\nmother\' brothers')
    [print(result) for result in results]