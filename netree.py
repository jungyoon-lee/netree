from base import Base, Tree
from myinfo import MyInfo
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

    print('My Network Interface      :', base.color_text('yellow', myinfo.network_interface))
    print(base.color_text('red', 'My IP Address             :'), base.color_text('red', myinfo.ip))
    print('My MAC Address            :', base.color_text('yellow', myinfo.mac))

    print('\nGateway IP Address        :', base.color_text('cyan', myinfo.gateway_ip))
    print('External IP Address       :', base.color_text('magenta', myinfo.external_ip))

    print('Useable IP                :', myinfo.get_ip_by_index(2),
                                     '~',
                                     myinfo.get_ip_by_index(-2))

    # print('\nDNS Server IP Address     :', '0.0.0.0')

    brothers = arp.scan()
    brothers_ips = [ip['ip-address'] for ip in brothers]

    info_table = PrettyTable(['IP Address', 'MAC Address', 'Product'])
    
    grandmother_ip = icmp.scan_grandmother()

    if grandmother_ip is None:
        grandmother_ip = '   NOT FOUND'
        mother_brothers = list()
        grand_router_address = '   NOT FOUND'
    else:
        mother_brothers, grand_router_address = icmp.scan_mother_brothers(grandmother_ip)
        
        for brother_ip in mother_brothers:
            if brother_ip == myinfo.gateway_ip:
                info_table.add_row([base.color_text('cyan', brother_ip), '', ''])
            elif brother_ip == grand_router_address or brother_ip == grandmother_ip:
                info_table.add_row([base.color_text('blue', brother_ip), '', ''])
            else:
                info_table.add_row([base.color_text('green', brother_ip), '', ''])

        if grand_router_address == myinfo.ip:
            grand_router_address = myinfo.external_ip
            mother_brothers = list()

        try:
            mother_brothers.remove(grandmother_ip)
        except Exception as error:
            pass
        
        try:
            mother_brothers.remove(grand_router_address)
        except Exception:
            pass

    for brother in brothers:
        if brother['ip-address'] == myinfo.gateway_ip:
            info_table.add_row([base.color_text('cyan', brother['ip-address']), 
                                base.color_text('cyan', brother['mac-address']), 
                                base.color_text('cyan', brother['product'])])
        elif brother['ip-address'] == myinfo.ip:
            info_table.add_row([base.color_text('red', brother['ip-address']), 
                                base.color_text('red', brother['mac-address']), 
                                base.color_text('red', brother['product'])])
        else:
            info_table.add_row([base.color_text('green', brother['ip-address']), 
                                base.color_text('green', brother['mac-address']), 
                                base.color_text('green', brother['product'])])

    try:
        brothers_ips.remove(myinfo.gateway_ip)
    except Exception as error:
        pass

    tree = Tree(my_ip=myinfo.ip,
                grandmother_ip1=myinfo.external_ip,
                grandmother_ip2=grandmother_ip,
                mother_brothers=mother_brothers,
                mother1        =grand_router_address,
                mother2        =myinfo.gateway_ip,
                brothers       =brothers_ips)
    tree.printTree()

    print(info_table)