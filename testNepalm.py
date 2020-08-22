from napalm import get_network_driver
from datetime import datetime
import time
import threading  # Now enabling ihe multi-threading
'''
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
'''

start = time.time()

def configsend(devices):
    connections = get_network_driver(**devices)
    ios.open()

    ios.load_merge_candidate('all_config.txt')

    deff = ios.compare_config()

    print(deff)


    ios.close()

with open('lab_routers.txt') as f:
    mydevices1 = f.read().splitlines()

# Creating a list here before for loop
threads1 = list()
for routers in mydevices1:
    optional_args = {'secret': 'cisco'}
    connections_driver = get_network_driver('ios')
    ios = connections_driver(routers,'admin', 'admin', optional_args=optional_args)

    #creating thread here
    th = threading.Thread(target=configsend, args=(ios, ) )
    threads1.append(th)

for th in threads1:
    th.start()

for th in threads1:
    th.join()



end = time.time()
print(f'Total time took to execution this script is: {end - start}')