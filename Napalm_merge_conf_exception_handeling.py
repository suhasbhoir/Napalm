from napalm import get_network_driver
from netmiko import NetMikoAuthenticationException
import json
from termcolor import colored
import time

start = time.time()
driver = get_network_driver('ios')
optional_args = {'secret': 'cisco'}
try:
    ios = driver('b2', 'suhas', 'cisco123', optional_args=optional_args)
    ios.open()
except NetMikoAuthenticationException:
    print('Authentication Error!!!')
else:
    ios.load_merge_candidate('nacl.txt')
    diff = ios.compare_config()
    print('Below configuration will be push on device')
    print((diff))

    while True:
        if len(diff) > 0:
            userinp = input('Do you want to commit changes on device, hit Y or  N: ').lower().strip()
            if userinp == 'y':
                ios.commit_config()
                print(colored('\nCommitting changes on devise', 'yellow'))
                print('#' * 50)
                print(colored('\nCommit confirm...', 'green'))
                break
            elif userinp == 'n':
                print(colored('\nDiscard the changes', 'red'))
                ios.discard_config()
                break
            else:
                print(colored('\ninvalid input detected', 'blue'))


    ios.close()
end = time.time()
print(f'Total time during execution is:', colored(end - start, 'red'))
