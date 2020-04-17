from struct import pack, unpack, error as struct_error

from socket import error as sock_error, inet_aton, inet_ntoa, inet_pton, htons, IPPROTO_TCP, IPPROTO_UDP, AF_INET6
from socket import socket, AF_PACKET, SOCK_RAW, inet_ntop, IPPROTO_ICMPV6

from binascii import unhexlify
from ipaddress import IPv4Address


def trans_bytes_mac(mac_address='01:23:34:45:56:67'):
    if len(mac_address) == 17 and type(mac_address) == str:
        return unhexlify(mac_address.replace(':', ''))

    elif len(mac_address) == 6 and type(mac_address) == bytes:
        result_mac_address: str = ''
        for byte_of_address in mac_address:
            result_mac_address += '{:02x}'.format(byte_of_address) + ':'
        return result_mac_address[:-1].lower()


def trans_bytes_ip(ip):
    ip = int(IPv4Address(ip))
    return ip.to_bytes(4, byteorder='big')


class EthernetPacket:
    def make_header(self, 
                    destination_mac=None,
                    source_mac=None,
                    network_type: int = 2054):
                        
        destination_mac = trans_bytes_mac(destination_mac)
        source_mac = trans_bytes_mac(source_mac)
        network_type = pack('!H', network_type)
        
        return destination_mac + source_mac + network_type

    
    def parse_packet(self, packet: bytes):
        try:
            assert not len(packet) != 14, \
                'Bad packet length: ' + \
                ' normal Ethernet header length: ' + '14'

            ethernet_detailed = unpack('!' '6s' '6s' 'H', packet)

            return {
                'destination': trans_bytes_mac(ethernet_detailed[0]),
                'source':      trans_bytes_mac(ethernet_detailed[1]),
                'type':        int(ethernet_detailed[2])
            }

        except AssertionError as Error:
            error_text = Error.args[0]

        except IndexError:
            error_text = 'Failed to parse Ethernet header!'


class ArpPacket:
    eth = EthernetPacket()
    
    def __init__(self):
        self.destination_mac = 'ff:ff:ff:ff:ff:ff'
        self.source_mac      = None
        self.sender_mac      = None
        self.sender_ip       = None
        self.target_mac      = '00:00:00:00:00:00'
        self.hw_type         = 1
        self.protocol_type   = 2048
        self.hw_length       = 6
        self.protocol_length = 4
        self.opcode          = 1
        self.network_type    = 2054


    def save_data(self,
                  destination_mac='ff:ff:ff:ff:ff:ff',
                  source_mac     ='12:34:56:78:9a:bc',
                  sender_mac     ='12:34:56:78:9a:bc',
                  sender_ip      ='192.168.0.1',
                  target_mac     ='00:00:00:00:00:00'):
        
        self.destination_mac = destination_mac
        self.source_mac = source_mac
        self.sender_mac = sender_mac
        self.sender_ip = sender_ip
        self.target_mac = target_mac


    def make_packet(self, target_ip='192.168.0.1'):

        eth_header = self.eth.make_header(destination_mac=self.destination_mac,
                                          source_mac     =self.source_mac,
                                          network_type   =self.network_type)
        arp_packet = b''
        arp_packet += pack('!H', self.hw_type)
        arp_packet += pack('!H', self.protocol_type)
        arp_packet += pack('!B', self.hw_length)
        arp_packet += pack('!B', self.protocol_length)
        arp_packet += pack('!H', self.opcode)
        arp_packet += trans_bytes_mac(self.sender_mac)
        arp_packet += trans_bytes_ip(self.sender_ip)
        arp_packet += trans_bytes_mac(self.target_mac)
        arp_packet += trans_bytes_ip(target_ip)

        return eth_header + arp_packet


    def make_requests(self, target_ip_addresses=None):
        arp_requests = list()

        for ip in target_ip_addresses:
            arp_requests.append(self.make_packet(ip))
        
        return arp_requests

    
    def parse_packet(self, packet: bytes):
        error_text: str = 'Failed to parse ARP packet!'
        try:
            assert not len(packet) != 28, \
                ' Bad packet length: ' + 'self.base.error_text(str(len(packet)))' + \
                ' normal ARP packet length: ' + 'self.base.success_text(str(RawARP.packet_length))'

            arp_detailed = unpack('!' '2H' '2B' 'H' '6s' '4s' '6s' '4s', packet)

            return {
                'hardware-type': int(arp_detailed[0]),
                'protocol-type': int(arp_detailed[1]),
                'hardware-size': int(arp_detailed[2]),
                'protocol-size': int(arp_detailed[3]),
                'opcode':        int(arp_detailed[4]),
                'sender-mac':    trans_bytes_mac(mac_address=arp_detailed[5]),
                'sender-ip':     inet_ntoa(arp_detailed[6]),
                'target-mac':    trans_bytes_mac(mac_address=arp_detailed[7]),
                'target-ip':     inet_ntoa(arp_detailed[8])
            }

        except AssertionError as Error:
            error_text += Error.args[0]

        except IndexError:
            pass