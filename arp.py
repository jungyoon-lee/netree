from packet import EthernetPacket, ArpPacket
from network import MyInfo

from ipaddress import IPv4Address
from socket import socket, AF_PACKET, SOCK_RAW, htons, error


class ArpScan:
    ethernet = EthernetPacket()
    arp = ArpPacket()

    rawSocket = socket(AF_PACKET, SOCK_RAW, htons(0x0003))

    interface = None
    my_mac = None
    my_ip = None
    mine = MyInfo()
    retries = 3

    arp_requests = list()
    results = list()

    def send(self):
        send_socket = socket(AF_PACKET, SOCK_RAW)
        send_socket.bind((self.interface, 0))

        for _ in range(self.retries):
            for arp_request in self.arp_requests:
                # print(arp_request)
                send_socket.send(arp_request)

        send_socket.close()


    def scan(self, 
             interface=None, 
             my_mac=None, 
             my_ip=None):
             
        self.arp_requests.clear()
        self.results.clear()

        self.interface = interface
        self.my_mac = my_mac
        self.my_ip = my_ip

        first_ip = self.mine.get_ip_by_index(interface, 1)
        last_ip = self.mine.get_ip_by_index(interface, -2)

        idx = 1
        while True:
            current_ip = self.mine.get_ip_by_index(interface, idx)

            idx += 1
            if IPv4Address(current_ip) > IPv4Address(last_ip):
                break

            arp_request = self.arp.make_request(destination_mac='ff:ff:ff:ff:ff:ff',
                                                source_mac=self.my_mac,
                                                sender_mac=self.my_mac,
                                                sender_ip=self.my_ip,
                                                target_mac='00:00:00:00:00:00',
                                                target_ip=current_ip)

            self.arp_requests.append(arp_request)

        self.send()