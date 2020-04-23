from socket import socket, AF_INET, SOCK_RAW, SOCK_DGRAM, IPPROTO_ICMP, IPPROTO_UDP, \
                    SOL_IP, IP_TTL, SOL_SOCKET, SO_RCVTIMEO, \
                    gethostbyaddr, gethostbyname, error, getprotobyname, htons

import struct
from time import time

if __name__ == '__main__':
    rece_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    timeout = struct.pack("ll", 5, 0)
    rece_socket.setsockopt(SOL_SOCKET, SO_RCVTIMEO, timeout)
    rece_socket.bind(("", 55285))

    live_addresses = list()
    start_time = time()

    while True:
        current_time = time()
        if (current_time - start_time) > 5:
            break

        try:
            _, curr_addr = rece_socket.recvfrom(512)
            
            if curr_addr[0] not in live_addresses:
                live_addresses.append(curr_addr[0])

        except Exception as error:
            print(error)

    rece_socket.close()

    print(live_addresses)