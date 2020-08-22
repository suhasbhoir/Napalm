from napalm import get_network_driver
import json

driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
ios = driver('b2', 'suhas', 'cisco123', optional_args=optional_args)
ios.open()

ios.load_replace_candidate(filename='b2-conf.txt')

diff = ios.compare_config()

if len(diff) > 0:
    print(diff)
    print('Commit changes on Device...')
    ios.commit_config()
    print('Commit Done successfully...')
else:
    ios.discard_config()
    print('No changes required')



ios.close()