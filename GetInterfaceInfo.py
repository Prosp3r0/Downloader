import os
import sys
import netifaces

#routingGateway = netifaces.gateways()[netifaces.AF_INET][0][]
routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
#os.system('sudo tcpdump -i en0')
for interface in netifaces.interfaces():
        #while interface
        #exit(0)
        #routingGateway = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['default']
        #routingNicName = netifaces.gateways()[interface][netifaces.AF_INET][1]
        #if interface == routingNicName:
        # print netifaces.ifaddresses(interface)
        #routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        #routingGateway = netifaces.gateways()[netifaces.AF_INET][0]
        #print (len(netifaces.gateways()[netifaces.AF_INET]))
        try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            if routingIPAddr != "127.0.0.1":
                i = 0
                while interface != netifaces.gateways()[netifaces.AF_INET][i][1]:
                        #print (i, len(netifaces.gateways()))
                        i = i + 1
                        if i == len(netifaces.gateways()[netifaces.AF_INET]):
                                i = i - 1
                                break
                routingGateway = netifaces.gateways()[netifaces.AF_INET][i][0]
            # (Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
                display_format = '%-30s %-20s'
                print (display_format % ("Routing Gateway:", routingGateway))
                print (display_format % ("Routing NIC Name:", interface))
            #print (display_format % ("Routing NIC MAC Address:", routingNicMacAddr))
                print (display_format % ("Routing IP Address:", routingIPAddr))
                print (display_format % ("Routing IP Netmask:", routingIPNetmask))
        except KeyError:
            pass
