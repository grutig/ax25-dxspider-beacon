#!/usr/bin/python3
import pythonax25
import os
import time

#####
# need python-ax25 https://github.com/josefmtd/python-ax25
# by Josef Matondang
####

def main():
    if pythonax25.config_load_ports() > 0:
        axport = pythonax25.config_get_first_port()
        axdevice = pythonax25.config_get_device(axport)
        axaddress = pythonax25.config_get_address(axport)
    else:
        exit(0)
    # Initiate a datagram socket
    socket = pythonax25.datagram_socket()
    srcCall = 'I8ZSE-1'
    portCall = axaddress
    res = pythonax25.datagram_bind(socket, srcCall, portCall)
    flash = "flash.txt"
    while True:
        if os.path.isfile(flash):
            lines = open(flash).readlines()
            for line in lines:
                line = line.strip("")
                if line != "":
                    dest = 'INFO'
                    digi = ''
                    msg = "\r\n".join(line.split("\t"))
                    res = pythonax25.datagram_tx_digi(socket, dest, digi, msg)
                    time.sleep(1)
            os.remove(flash)
        time.sleep(1)

if __name__ == '__main__':
    main()
