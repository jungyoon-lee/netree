from packet import ArpPacket
from network import MyInfo

from ipaddress import IPv4Address
from socket import socket, AF_PACKET, SOCK_RAW, htons, error


class ArpScan:
    def __init__(self, myinfo : MyInfo):
        self.arp = ArpPacket()    
        self.myinfo : MyInfo = myinfo

        self.retries = 3
        self.arp_requests = list()
        self.results = list()
        self.ip_addresses = list()


    def send(self):
        send_socket = socket(AF_PACKET, SOCK_RAW)
        send_socket.bind((self.myinfo.network_interface, 0))

        for _ in range(self.retries):
            for arp_request in self.arp_requests:
                send_socket.send(arp_request)

        send_socket.close()


    def scan(self):
        self.results.clear()
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

        self.send()