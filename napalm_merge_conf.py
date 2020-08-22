from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('b2', 'suhas', 'cisco123', optional_args=optional_args)
ios.open()

ios.load_merge_candidate('acl.txt')

diff = ios.compare_config()
print('Below configuration will be push on device')
print((diff))

while True:
    if len(diff) > 0:
        userinp = input('Do you want to commit changes on device, Y or  N: ').lower().strip()
        if userinp == 'y':
            ios.commit_config()
            print('Committing changes on devise')
            break
        elif userinp == 'n':
            print('Discard the changes')
            ios.discard_config(), ios.
            break
        else:
            print('invalid input detected')


ios.close()