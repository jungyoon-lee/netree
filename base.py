from os.path import dirname, abspath, isfile, join
from colorama import init, Fore, Style
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
            "|_| |_|  \___|   |___| |_|    \___|  \___|   \n"


    def print_banner(self):
        green_banner = self.color_text('green', self.get_banner())
        print(green_banner)


    def color_text(self, color, string):
        result_string = ''

        if color == 'blue':
            result_string += Style.BRIGHT + Fore.BLUE
        elif color == 'red':
            result_string += Style.BRIGHT + Fore.RED
        elif color == 'green':
            result_string += Style.BRIGHT + Fore.GREEN

        result_string += string
        result_string += Style.RESET_ALL

        return result_string
        

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
    def __init__(self, my_ip,
                       grandmother_ip1, 
                       grandmother_ip2, 
                       mother_brothers, 
                       mother1,
                       mother2, 
                       brothers):
        self.my_ip=my_ip
        self.grandmother_ip1 = grandmother_ip1
        self.grandmother_ip2 = grandmother_ip2
        self.mother_brothers = mother_brothers
        self.mother1 = mother1
        self.mother2 = mother2
        self.brothers = brothers

        self.start_pot2 = int(len(self.brothers) * 19 / 2) - 9
        self.start_pot1 = self.start_pot2 + int((len(self.mother_brothers) + 1) * 19 / 2) - 9

        self.base = Base()


    def printTree(self):
        print("===============================================================================")
        if self.grandmother_ip1 != self.mother2:
            self.prtGrandmother(ip1=self.grandmother_ip1, 
                                ip2=self.grandmother_ip2, 
                                start_pot1=self.start_pot1,
                                start_pot2=self.start_pot2,
                                sons=self.mother_brothers)
        self.prtMother(ip1=self.mother1, 
                       ip2=self.mother2, 
                       brothers=self.mother_brothers, 
                       start_pot=self.start_pot2,
                       sons=self.brothers)
        self.prtBrothers(my_ip=self.my_ip, brothers=self.brothers)
        print("===============================================================================")

    
    def prtGrandmother(self, ip1, ip2, start_pot1, start_pot2, sons):
        '''
                                                       ///////////////// 
                                                       /               /
                                                       /               /
                                                       /////////////////
                                                               |
                                                               |
                                            +------------------+------------------+
                                            |                  |                  |
                                            |                  |                  |
        '''
        router_top    = " ///////////////// "
        router_middle = " /               / "
        router_bottom = " ///////////////// "
        bar           = "         |         "

        # region top
        print('')
        stdout.write(' ' * start_pot1)
        stdout.write(self.base.color_text('blue', router_top))

        # middle
            # outer
        print('')
        stdout.write(' ' * start_pot1)
        stdout.write(self.base.color_text('blue', router_middle[:2]))
        stdout.write(self.base.color_text('blue', ip1))
        stdout.write(self.base.color_text('blue', router_middle[len(ip1) + 2:]))
            # router
        print('')
        stdout.write(' ' * start_pot1)
        stdout.write(self.base.color_text('blue', router_middle[:2]))
        stdout.write(self.base.color_text('blue', ip2))
        stdout.write(self.base.color_text('blue', router_middle[len(ip2) + 2:]))

        # bottom
        print('')
        stdout.write(' ' * start_pot1)
        stdout.write(self.base.color_text('blue', router_bottom))
        # endregion top
        
        #          |
        #          |
        print('')
        stdout.write(' ' * start_pot2)
        stdout.write(' ' * int((len(sons) + 1) * 19 / 2))
        stdout.write('|')
        print('')
        stdout.write(' ' * start_pot2)
        stdout.write(' ' * int((len(sons) + 1) * 19 / 2))
        stdout.write('|')

        #     +----+----+
        if len(sons) > 0:
            print('')
            stdout.write(' ' * (start_pot2 + 9))
            stdout.write('+')
            for _ in range(len(sons)):
                stdout.write('-' * 18 + '+')
            # |    |    |     
            # |    |    |
            print('')
            stdout.write(' ' * start_pot2)
            for _ in range(len(sons) + 1):
                stdout.write(bar)
            print('')
            stdout.write(' ' * start_pot2)
            for _ in range(len(sons) + 1):
                stdout.write(bar)


    def prtMother(self, ip1, ip2, brothers, start_pot, sons):
        '''
                                   /////////////////  +-------+-------+  +-------+-------+  
                                   /               /  |               |  |               | 
                                   /               /  |               |  |               |  
                                   /////////////////  +-------+-------+  +-------+-------+  
                                            |
                                            |
                +------------------+------------------+------------------+
                |                  |                  |                  |
                |                  |                  |                  |
        '''
        bar           = "         |         "
        router_top    = " ///////////////// "
        router_middle = " /               / "
        router_bottom = " ///////////////// "
        device_top    = " +-------+-------+ "
        device_middle = " |               | "
        device_bottom = " +---------------+ "

        # region top
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(self.base.color_text('blue', router_top))
        for _ in brothers:
            stdout.write(device_top)

        # middle 1
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(self.base.color_text('blue', router_middle[:2]))
        stdout.write(self.base.color_text('blue', ip2))
        stdout.write(self.base.color_text('blue', router_middle[len(ip2) + 2:]))
            # device
        for brother in brothers:
            stdout.write(device_middle[:2])
            stdout.write(brother)
            stdout.write(device_middle[len(brother) + 2:])

        # middle 2
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(self.base.color_text('blue', router_middle[:2]))
        stdout.write(self.base.color_text('blue', ip1))
        stdout.write(self.base.color_text('blue', router_middle[len(ip1) + 2:]))
            # device
        for _ in brothers:
            stdout.write(device_middle)
        
        # bottom
            # router
        print('')
        stdout.write(' ' * start_pot)
        stdout.write(self.base.color_text('blue', router_bottom))
            # device
        for _ in brothers:
            stdout.write(device_bottom)
        # endregion top

        # |
        # |
        print('')
        stdout.write(' ' * int(len(sons) * 19 / 2))
        stdout.write('|')
        print('')
        stdout.write(' ' * int(len(sons) * 19 / 2))
        stdout.write('|')

        if len(sons) > 1:
            print('')
            stdout.write(' ' * 9)
            stdout.write('+')
            for _ in range(len(sons) - 1):
                stdout.write('-' * 18 + '+')
            print('')
            for _ in sons:
                stdout.write(bar)
            print('')
            for _ in sons:
                stdout.write(bar)

    
    def prtBrothers(self, my_ip, brothers):
        '''
        +-------+-------+  +-------+-------+  +-------+-------+  +-------+-------+
        |               |  |               |  |               |  |               |
        |               |  |               |  |               |  |               |
        +---------------+  +---------------+  +---------------+  +-------+-------+
        '''
        top    = " +-------+-------+ "
        middle = " |               | "
        bottom = " +---------------+ "

        # top
        print('')
        for brother_ip in brothers:
            if brother_ip == my_ip:
                stdout.write(self.base.color_text('red', top))
            else:
                stdout.write(top)

        # middle
        print('')
        for brother_ip in brothers:
            if brother_ip == my_ip:
                stdout.write(self.base.color_text('red', middle))
            else:
                stdout.write(middle)

        print('')
        for brother_ip in brothers:
            if brother_ip == my_ip:
                stdout.write(self.base.color_text('red', middle[:2]))
                stdout.write(self.base.color_text('red', brother_ip))
                stdout.write(self.base.color_text('red', middle[len(brother_ip) + 2:]))
            else:
                stdout.write(middle[:2])
                stdout.write(brother_ip)
                stdout.write(middle[len(brother_ip) + 2:])

        # bottom
        print('')
        for brother_ip in brothers:
            if brother_ip == my_ip:
                stdout.write(self.base.color_text('red', bottom))
            else:
                stdout.write(bottom)
        print('')