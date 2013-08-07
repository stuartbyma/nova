#Copyright (C) 2012, The SAVI Project.

__author__ = 'Bo Bao (bob.bao@mail.utoronto.ca)'
__author__ = 'Hesam, Rahimi Koopayi (hesam.rahimikoopayi@utoronto.ca)'
__author__ = 'Stuart, Byma (stuart.byma@utoronto.ca)'

import socket
import os
from nova import exception

#from libs.customized_logging import logger

def pr_virt_tcp (cmd, mac_address, subagent_address, dir_path=0):
    result = "OK"
    # open a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect(("", 6677))
    subagent_address_components = subagent_address.split(":")
    subagent_ip_address = subagent_address_components[0]
    subagent_port = subagent_address_components[1]
    
    try: 
        client_socket.connect((subagent_ip_address, int(subagent_port)))
        client_socket.settimeout(10)
    except: 
        raise exception.NovaException('TCP CONNETION DIED')
    
    #send request
    try:
        print("TCP SEND COMMAND:"+cmd)
        client_socket.send(cmd + "\r\n")
        if (cmd == "PRG"):
            size = str(os.path.getsize(dir_path))
            print ("FPGA-IMAGE size is=%s", size)
            client_socket.send(str(size) + "\r\n")
            #mac_address = "23:45:67:89:ab:cd"
            print ("FPGA-REGION-MAC-ADDRESS is=%s", mac_address)
            client_socket.send(mac_address + "\r\n")
            #client_socket.send("\r\n")

            bit_file = open(dir_path)
            data = bit_file.read(1024)
            while (data != ""):
                client_socket.send(data)
                data = bit_file.read(1024)
        elif cmd == "REL":
            client_socket.send(mac_address + "\r\n")


            
    except socket.timeout:
        result = -1
        message = "socket timeout"

    #wait for response
    if (result == "OK"):
        try:
            response = client_socket.recv(512)
            print("The response is :" + response)
            if (response == ""):
                result = -1
                message = "not receive response before closing connection"
            else:
                response_array = response.split("\r\n")
                print len(response_array)
                if (len(response_array) != 3):
                    result = -1
                    message = "response message is too long or in incorrect format"
                else:
                    result = response_array[0]
                    message = response_array[1]
                    
        except socket.timeout:
            result = -1
            message = "socket timeout"

    print("Result is:" + str(result))
    print("Message is :" + str(message))
    return result, message
