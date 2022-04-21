#!/usr/bin/python3

import pythonax25
import datetime

#####
# need python-ax25 https://github.com/josefmtd/python-ax25
# by Josef Matondang
####

def parsePacket(string):
	# Split the address and payload separated by APRS PID
	buffer = string.split(b'\x03\xf0')
	address = buffer[0]

	# Check if the first byte indicates it is a data packet
	if address[0] is 0:
		# Cut the first byte and feed it to the address parser
		listAddress = getAllAddress(address[1:])

		# Get the source, destination, and digipeaters from the address list
		source = listAddress[1]
		destination = listAddress[0]
		digipeaters = listAddress[2:]
	else:
		raise Exception('Not a data packet')

	payload = buffer[1]
	return (source, destination, digipeaters, payload)

def getAllAddress(packetAddress):
	addressSize = 7
	# Check if the networked address string is valid
	if (len(packetAddress) % 7) is 0:
		# Create a list of all address in ASCII form
		allAddress = [pythonax25.network_to_ascii(packetAddress[i:i+addressSize])
            for i in range(0, len(packetAddress), addressSize)]
		return allAddress
	else:
		raise Exception('Error: Address is not a multiple of 7')

def main():
    # Check if there's any active AX25 port
    if pythonax25.config_load_ports() > 0:
        # Get the device name of the first port
        axport = pythonax25.config_get_first_port()
        axdevice = pythonax25.config_get_device(axport)
        axaddress = pythonax25.config_get_address(axport)
    else:
        exit(0)

    # Initiate a PF_PACKET socket
    socket = pythonax25.packet_socket()

    while True:
        # Blocking receive packet, 10 ms timeout
        receive = pythonax25.packet_rx(socket, 100)
        if receive[0][1] == axdevice:
            try:
               source, destination, digipeaters, payload = parsePacket(receive[1])
               msg = payload.decode().strip().upper()
            except:
               msg = ""
            msg += " "
            if msg[0:10] == "DXCLUSTER ":
                buf = ""
                dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S | ')
                open("rx.log","a").write(dt+" "+source+">"+destination+":"+msg+"\n")
                parms = msg[10:].strip()
                if parms == "HELP":
                    open("help.sem", "w").write("")
                    break
                flts = parms.strip().split(" ")
                for flt in flts:
                    if flt in ["160", "60", "40", "30", "20", "17", "15", "12", "10", "LSB", "USB", "CW", "DIGITAL", ""]:
                        buf += flt+" "
                    else:
                        open("flash.txt", "a").write("DxCluster - filtro non valido: " + flt+"\n")
                        break
                open("filters.dat", "w").write(buf)
                if buf.strip() == "": 
                   buf = "nessuno"
                open("flash.txt", "a").write("DxCluster - filtri attivi: " + buf+"\n")
        else:
            continue

main()
