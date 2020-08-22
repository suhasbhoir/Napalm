from napalm import get_network_driver
import json
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import time
import threading  # Now enabling ihe multi-threading
'''upgrade la
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
'''

start = time.time()

def configsend(devices):
    driver = get_network_driver('ios')
    connections = get_network_driver(**devices)
    connections.open()

    connections.get_facts()
    bgp_neigh = connections.get_bgp_neighbors()


    print('\nApplying configuration to devices from file...\n')
    router = connections.send_config_from_file('config.txt')
    print(router)


    print('\nclosing the connection')
    connections.disconnect()


with open('mydevices.txt') as f:
    mydevices1 = f.read().splitlines()

# Creating a list here before for loop
threads1 = list()
for ip in mydevices1:
    cisco_devices = {
                     'device_type': 'cisco_ios',
                     'host': ip,
                     'username': 'admin',
                     'password': 'admin',
                     'port': '22',
                     'secret': 'cisco',
                     'verbose': True
                      }

    #creating thread here
    try:
        th = threading.Thread(target=configsend, args=(cisco_devices, ) )
        threads1.append(th)
    except (AuthenticationException):
        print('Authentication failure: ' + ip)
        continue
    except(NetMikoTimeoutException):
        print('Timeout to device: ' + ip)
        continue
    except(EOFError):
        print("End of file while attempting device " + ip)
        continue
    except(SSHException):
        print('SSH Issue. Are you sure SSH is enabled? ' + ip)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue

for th in threads1:
    th.start()

for th in threads1:
    th.join()



end = time.time()
print(f'Total time took to execution this script is: {end - start}')