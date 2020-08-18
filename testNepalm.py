from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('b2', 'admin', 'admin', optional_args=optional_args)
ios.open()

output = ios.get_arp_table(), ios.get_interfaces()
# for item in output:
#     print(item)

dump = json.dumps(output, sort_keys=True, indent=4)
# print(dump)

with open('arp_output.txt', 'w') as f:
    f.write(dump)


ios.close()