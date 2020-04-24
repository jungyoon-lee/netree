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

    brothers = arp.scan()
    brothers_ips = [ip['ip-address'] for ip in brothers]

    brother_table = PrettyTable(['IP Address', 'MAC Address', 'Product'])
        
    for brother in brothers:
        brother_table.add_row([brother['ip-address'], brother['mac-address'], brother['product']])
    
    grandmother_ip = icmp.scan_grandmother()
    mother_brothers_table = PrettyTable(['IP Address'])

    if grandmother_ip is None:
        grandmother_ip = '   NOT FOUND'
        mother_brothers = list()
        grand_router_address = '   NOT FOUND'
    else:
        mother_brothers, grand_router_address = icmp.scan_mother_brothers(grandmother_ip)

        for brother in mother_brothers:
            mother_brothers_table.add_row([brother])

        mother_brothers.remove(grandmother_ip)
        mother_brothers.remove(grand_router_address)

    brothers_ips.remove(myinfo.gateway_ip)

    tree = Tree(grandmother_ip1='   NOT FOUND',
                grandmother_ip2=grandmother_ip,
                mother_brothers=mother_brothers,
                mother1        =myinfo.gateway_ip,
                mother2        =grand_router_address,
                brothers       =brothers_ips)
    tree.printTree()

    print(mother_brothers_table)
    print(brother_table)