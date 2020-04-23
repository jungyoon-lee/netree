from socket import socket, AF_INET, SOCK_RAW, SOCK_DGRAM, IPPROTO_ICMP, IPPROTO_UDP, \
                    SOL_IP, IP_TTL, SOL_SOCKET, SO_RCVTIMEO, \
                    gethostbyaddr, gethostbyname, error, getprotobyname, htons

from packet import IcmpPacket
import struct
from tm import ThreadManager
from time import time


class IcmpScan:
    def __init__(self):
        self.live_addresses = list()
        self.receive_finish = False


    def receive(self):
        port = 55285

        rece_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        timeout = struct.pack("ll", 5, 0)
        rece_socket.setsockopt(SOL_SOCKET, SO_RCVTIMEO, timeout)
        rece_socket.bind(("", port))

        start_time = time()

        while True:
            current_time = time()
            if (current_time - start_time) > 5:
                break

            try:
                _, curr_addr = rece_socket.recvfrom(512)
                # print(_)
                
                if curr_addr[0] not in self.live_addresses:
                    self.live_addresses.append(curr_addr[0])

            except Exception as error:
                pass

        rece_socket.close()
        self.receive_finish = True


    def send(self, addresses):
        icmp = IcmpPacket()
        packet = icmp.make_packet()

        my_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

        for address in addresses:
            my_socket.sendto(packet, (address, 1))

        my_socket.close()

    
    def scan_mother_brothers(self, 
                             router_address="192.168.0.1",
                             start_index=1,
                             end_index=255):
                             
        for idx in range(len(router_address)):
            if router_address[idx] == '.':
                dot = idx

        prefix_address = router_address[:dot+1]

        addresses = [prefix_address + str(idx) for idx in range(start_index, end_index + 1)]

        tm = ThreadManager(2)
        tm.add_task(self.receive)

        self.send(addresses)

        while True:
            if self.receive_finish == True:
                return self.live_addresses


    def scan_grandmother(self):
        dest_name = "www.naver.com"
        curr_addr = None
        port = 55285
        ttl = 2

        rece_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        send_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        send_socket.setsockopt(SOL_IP, IP_TTL, ttl)

        timeout = struct.pack("ll", 5, 0)
        rece_socket.setsockopt(SOL_SOCKET, SO_RCVTIMEO, timeout)
        rece_socket.bind(("", port))

        send_socket.sendto(bytes("", "utf-8"), (dest_name, port))

        _, curr_addr = rece_socket.recvfrom(512)

        rece_socket.close()
        send_socket.close()

        return curr_addr[0]