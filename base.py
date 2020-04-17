from os.path import dirname, abspath, isfile, join

class Base:
    def __init__(self):
        self.abc = 1
        self.vendor_list = list()

    def get_banner(self):
        return \
            "                  _                          \n" + \
            " _ __     ___   _| |_   _ __    __     __    \n" + \
            "|  _ \   / _ \ |_   _| | '__| / _ \  / _ \   \n" + \
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