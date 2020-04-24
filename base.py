from os.path import dirname, abspath, isfile, join
from sys import stdout

class Base:
    def __init__(self):
        self.abc = 1
        self.vendor_list = list()

    def get_banner(self):
        return \
            "                  _                          \n" + \
            " _ __     ___   _| |_   _ __    __     __    \n" + \
            "| '_ \   / _ \ |_   _| | '__| / _ \  / _ \   \n" + \
            "| | | | (  __/   | |_  | |   (  __/ (  __/   \n" + \
            "|_| |_|  \___|   |___| |_|    \___|  \___|   \n\n"


    def print_banner(self):
        print(self.get_banner())


    def get_mac_prefixes(self, prefixes_filename='mac-prefixes.txt'):
        assert len(self.vendor_list) == 0, 'Vendor list already exist!'
        try:
            if not isfile(prefixes_filename):
                prefixes_filename = join(dirname(abspath(__file__)), prefixes_filename)
                assert isfile(prefixes_filename), \
                    'File with MAC addresses list: ' + self.error_text(prefixes_filename) + ' not found!'
            with open(prefixes_filename, 'r') as mac_prefixes_descriptor:
                for mac_and_vendor_string in mac_prefixes_descriptor.read().splitlines():
                    mac_and_vendor_list = mac_and_vendor_string.split('\t')
                    try:
                        self.vendor_list.append({
                            'prefix': mac_and_vendor_list[0],
                            'vendor': mac_and_vendor_list[2]
                        })
                    except IndexError:
                        self.vendor_list.append({
                            'prefix': mac_and_vendor_list[0],
                            'vendor': mac_and_vendor_list[1]
                        })
        except AssertionError:
            pass
        return self.vendor_list


    def get_vendor_by_mac_address(self, mac_address='01:23:45:67:89:0a'):
        if len(self.vendor_list) == 0:
            self.get_mac_prefixes()
        
        mac_address: str = mac_address.upper()
        
        for vendor_dictionary in self.vendor_list:
            if len(vendor_dictionary['prefix']) == 8:
                if vendor_dictionary['prefix'] in mac_address:
                    return vendor_dictionary['vendor']
        return 'Unknown vendor'


class Tree:
    def __init__(self, grandmother_ip1, 
                       grandmother_ip2, 
                       mother_brothers, 
                       mother1,
                       mother2, 
                       brothers):
        self.grandmother_ip1 = grandmother_ip1
        self.grandmother_ip2 = grandmother_ip2
        self.mother_brothers = mother_brothers
        self.mother1 = mother1
        self.mother2 = mother2
        self.brothers = brothers

        self.start_pot2 = int(len(self.brothers) * 19 / 2) - 9
        self.start_pot1 = self.start_pot2 + int((len(self.mother_brothers) + 1) * 19 / 2) - 9


    def printTree(self):
        self.prtGrandmother(ip1=self.grandmother_ip1, 
                            ip2=self.grandmother_ip2, 
                            start_pot=self.start_pot1)
        self.prtMother(ip1=self.mother1, 
                       ip2=self.mother2, 
                       brothers=self.mother_brothers, 
                       start_pot=self.start_pot2)
        self.prtBrothers(brothers=self.brothers)


    def prtGrandmother(self, ip1, ip2, start_pot):
        '''
         ///////////////// 
         /               /
         /               /
         /////////////////
        '''
        router_top    = " ///////////////// "
        router_middle = " /               / "
        router_bottom = " ///////////////// "

        # top
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_top)

        # middle
            # outer
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_middle[:2])
        stdout.write(ip1)
        stdout.write(router_middle[len(ip1) + 2:])
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_middle[:2])
        stdout.write(ip2)
        stdout.write(router_middle[len(ip2) + 2:])

        # bottom
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_bottom)


    def prtMother(self, ip1, ip2, brothers, start_pot):
        '''
                                                        |
                                                        |
                            +------------------+------------------+------------------+
        |---------|         |                  |                  |                  |
         start pot          |                  |                  |                  |
                    /////////////////  +-------+-------+  +-------+-------+  +-------+-------+ 
                    /               /  |               |  |               |  |               |
                    /               /  |               |  |               |  |               |
                    /////////////////  +-------+-------+  +-------+-------+  +-------+-------+ 
        '''
        bar           = "         |         "

        router_top    = " ///////////////// "
        router_middle = " /               / "
        router_bottom = " ///////////////// "

        device_top    = " +-------+-------+ "
        device_middle = " |               | "
        device_bottom = " +---------------+ "

        #
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(' ' * int((len(brothers) + 1) * 19 / 2))
        stdout.write('|')
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(' ' * int((len(brothers) + 1) * 19 / 2))
        stdout.write('|')

        # +----+----+
        print('')
        stdout.write(' ' * (start_pot + 9))
        stdout.write('+')
        for _ in range(len(brothers)):
            stdout.write('-' * 18 + '+')

        # bar
        print('')
        stdout.write(' ' * start_pot)
        for _ in range(len(brothers) + 1):
            stdout.write(bar)
        print('')
        stdout.write(' ' * start_pot)
        for _ in range(len(brothers) + 1):
            stdout.write(bar)

        # top
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_top)
        for _ in brothers:
            stdout.write(device_top)

        # middle 1
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_middle[:2])
        stdout.write(ip2)
        stdout.write(router_middle[len(ip2) + 2:])
            # device
        for brother in brothers:
            stdout.write(device_middle[:2])
            stdout.write(brother)
            stdout.write(device_middle[len(brother) + 2:])

        # middle 2
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_middle[:2])
        stdout.write(ip1)
        stdout.write(router_middle[len(ip1) + 2:])
            # device
        for _ in brothers:
            stdout.write(device_middle)
        
        # bottom
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(router_bottom)
            # device
        for _ in brothers:
            stdout.write(device_bottom)


    def prtBrothers(self, brothers):
        '''
                                    |
                                    |
                 +------------------+------------------+
                 |                  |                  |
                 |                  |                  |
         +-------+-------+  +-------+-------+  +-------+-------+
         |               |  |               |  |               |
         |               |  |               |  |               |
         +-------+-------+  +-------+-------+  +-------+-------+

        '''
        bar    = "         |         "
        top    = " +-------+-------+ "
        middle = " |               | "
        bottom = " +---------------+ "

        print('')
        stdout.write(' ' * int(len(brothers) * 19 / 2))
        stdout.write('|')
        print('')
        stdout.write(' ' * int(len(brothers) * 19 / 2))
        stdout.write('|')
        
        print('')
        stdout.write(' ' * 9)
        stdout.write('+')
        for _ in range(len(brothers) - 1):
            stdout.write('-' * 18 + '+')
        print('')
        for _ in brothers:
            stdout.write(bar)
        print('')
        for _ in brothers:
            stdout.write(bar)

        # top
        print('')
        for _ in brothers:
            stdout.write(top)

        # middle
        print('')
        for _ in brothers:
            stdout.write(middle)

        print('')
        for ip in brothers:
            stdout.write(middle[:2])
            stdout.write(ip)
            stdout.write(middle[len(ip) + 2:])

        # bottom
        print('')
        for _ in range(len(brothers)):
            stdout.write(bottom)
        print('')