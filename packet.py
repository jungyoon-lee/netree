from struct import pack, unpack, error as struct_error

from socket import error as sock_error, inet_aton, inet_ntoa, inet_pton, htons, IPPROTO_TCP, IPPROTO_UDP, AF_INET6
from socket import socket, AF_PACKET, SOCK_RAW, inet_ntop, IPPROTO_ICMPV6

from binascii import unhexlify
from ipaddress import IPv4Address


class EthernetPacket:
    def trans_bytes_mac(self, 
                    mac_address=None):

        return unhexlify(mac_address.replace(':', ''))


    def make_header(self, 
                    destination_mac=None,
                    source_mac=None,
                    network_type: int = 2054):
                        
        destination_mac = self.trans_bytes_mac(destination_mac)
        source_mac = self.trans_bytes_mac(source_mac)
        network_type = pack('!H', network_type)
        
        return destination_mac + source_mac + network_type


class ArpPacket:
    eth = EthernetPacket()

    def trans_bytes_ip(self, ip):
        ip = int(IPv4Address(ip))
        return ip.to_bytes(4, byteorder='big')


    def make_packet(self,
                    destination_mac=None,
                    source_mac=None,
                    hw_type=None,
                    protocol_type=None,
                    hw_length=None,
                    protocol_length=None,
                    opcode=None,
                    sender_mac=None,
                    sender_ip=None,
                    target_mac=None,
                    target_ip=None):

        eth_header = self.eth.make_header(destination_mac=destination_mac,
                                          source_mac=source_mac,
                                          network_type = 2054)

        arp_packet = b''
        arp_packet += pack('!H', hw_type)
        arp_packet += pack('!H', protocol_type)
        arp_packet += pack('!B', hw_length)
        arp_packet += pack('!B', protocol_length)
        arp_packet += pack('!H', opcode)
        arp_packet += self.eth.trans_bytes_mac(sender_mac)
        arp_packet += self.trans_bytes_ip(sender_ip)
        arp_packet += self.eth.trans_bytes_mac(target_mac)
        arp_packet += self.trans_bytes_ip(target_ip)

        return eth_header + arp_packet


    def make_request(self,
                     destination_mac=None,
                     source_mac=None,
                     sender_mac=None,
                     sender_ip=None,
                     target_mac=None,
                     target_ip=None):

        return self.make_packet(destination_mac=destination_mac,
                                source_mac=source_mac,
                                hw_type=1,
                                protocol_type=2048,
                                hw_length=6,
                                protocol_length=4,
                                opcode=1,
                                sender_mac=sender_mac,
                                sender_ip=sender_ip,
                                target_mac=target_mac,
                                target_ip=target_ip)