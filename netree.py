from base import Base, Tree
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

    # start_arp_scan = time()
    brothers = arp.scan()
    brothers_ips = [ip['ip-address'] for ip in brothers]
    # end_arp_scan = time()

    brother_table = PrettyTable(['IP Address', 'MAC Address', 'Product'])
        
    for brother in brothers:
        brother_table.add_row([brother['ip-address'], brother['mac-address'], brother['product']])
    print(brother_table)
    # print(int(end_arp_scan - start_arp_scan), 'sec')
    
    grandmother_ip = icmp.scan_grandmother()
    mother_brothers, grand_router_address = icmp.scan_mother_brothers(grandmother_ip)

    brothers_ips.remove(myinfo.gateway_ip)
    mother_brothers.remove(grandmother_ip)
    mother_brothers.remove(grand_router_address)

    tree = Tree('',
                grandmother_ip,
                mother_brothers,
                myinfo.gateway_ip,
                grand_router_address,
                brothers_ips)
    tree.printTree()