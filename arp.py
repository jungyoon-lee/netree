from base import Base
from myinfo import MyInfo
from packet import ArpPacket, EthernetPacket
from tm import ThreadManager

from ipaddress import IPv4Address
from socket import socket, AF_PACKET, SOCK_RAW, htons, error

from operator import itemgetter # sorted

from time import sleep


class ArpScan:
    def __init__(self, myinfo : MyInfo):
        self.base = Base()
        self.arp = ArpPacket()
        self.eth = EthernetPacket()
        self.myinfo = myinfo

        self.rawSocket: socket = socket(AF_PACKET, SOCK_RAW, htons(0x0003))

        self.retries = 3
        self.arp_requests = list()
        self.results = list()
        self.real_results = list()
        self.ip_addresses = list()
        self.mac_addresses = list()

        self.timeout = 10


    def sniff(self):
        while True:
            packets = self.rawSocket.recvfrom(2048)
            for packet in packets:
                try:
                    ethernet_header = packet[0:14]
                    ethernet_header_dict = self.eth.parse_packet(ethernet_header)

                    assert ethernet_header_dict is not None, 'ethernet packet 실종'
                    
                    assert ethernet_header_dict['type'] == 2054, 'arp packet 아님'

                    assert ethernet_header_dict['destination'] == self.myinfo.mac.lower(), '너한테 보내진거 아님'
                    
                    arp_header = packet[14:42]
                    arp_header_dict = self.arp.parse_packet(arp_header)

                    assert arp_header_dict is not None, 'ARP packet 실종'

                    assert arp_header_dict['opcode'] == 2, 'Not ARP reply packet!'

                    assert arp_header_dict['target-mac'] == self.myinfo.mac.lower(), 'Not your ARP reply packet!'
                    
                    assert arp_header_dict['target-ip'] == self.myinfo.ip, 'Not your ARP reply packet!'
                    
                    self.results.append({
                        'mac-address': arp_header_dict['sender-mac'],
                        'ip-address': arp_header_dict['sender-ip']
                    })
                        
                except AssertionError:
                    pass


    def send(self):
        send_socket = socket(AF_PACKET, SOCK_RAW)
        send_socket.bind((self.myinfo.network_interface, 0))

        for _ in range(self.retries):
            for arp_request in self.arp_requests:
                send_socket.send(arp_request)

        send_socket.close()


    def scan(self):
        self.results.clear()
        self.real_results.clear()
        self.mac_addresses.clear()
        self.arp_requests.clear()

        last_ip = self.myinfo.get_ip_by_index(-2)

        idx = 1
        while True:
            current_ip = self.myinfo.get_ip_by_index(idx)

            idx += 1
            if IPv4Address(current_ip) > IPv4Address(last_ip):
                break

            self.ip_addresses.append(current_ip)

        self.arp.save_data(destination_mac='ff:ff:ff:ff:ff:ff',
                           source_mac=self.myinfo.mac,
                           sender_mac=self.myinfo.mac,
                           sender_ip=self.myinfo.ip,
                           target_mac='00:00:00:00:00:00')

        self.arp_requests = self.arp.make_requests(target_ip_addresses=self.ip_addresses)

        tm = ThreadManager(2)
        tm.add_task(self.sniff)

        self.send()

        sleep(self.timeout)

        self.results.append({
            'mac-address': self.myinfo.mac,
            'ip-address': self.myinfo.ip
        })

        for idx in range(len(self.results)):
            if self.results[idx]['mac-address'] not in self.mac_addresses:
                self.mac_addresses.append(self.results[idx]['mac-address'])
                self.real_results.append(self.results[idx])

        self.real_results = sorted(self.real_results, key=itemgetter('ip-address'))

        for result_idx in range(len(self.real_results)):
            self.real_results[result_idx]['product'] = \
                self.base.get_vendor_by_mac_address(self.real_results[result_idx]['mac-address'])

        return self.real_results