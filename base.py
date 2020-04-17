class Base:
    def __init__(self):
        self.abc = 1

    def get_banner(self):
        return \
            "                  _                          \n" + \
            " _ __     ___   _| |_   _ __    __     __    \n" + \
            "|  _ \   / _ \ |_   _| | '__| / _ \  / _ \   \n" + \
            "| | | | (  __/   | |_  | |   (  __/ (  __/   \n" + \
            "|_| |_|  \___|   |___| |_|    \___|  \___|   \n\n"


    def print_banner(self):
        print(self.get_banner())