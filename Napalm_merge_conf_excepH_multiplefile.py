from napalm import get_network_driver
from netmiko import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import json
from termcolor import colored
import time

start = time.time()
username = input('username: ')
password = getpass('password:')
driver = get_network_driver('ios')

with open('mydevices.txt', 'r') as router_ips:
    for ip in router_ips:
        print('connecting to', ip)
        optional_args = {'secret': 'cisco'}
        try:
            ios = driver(ip, username, password,  optional_args={'global_delay_factor': 4})
            ios.open()
        except NetMikoAuthenticationException:
            print(colored('Authentication Error!!!', 'red'))
            username = input('username: ')
            password = getpass('password:')
            ios = driver(ip, username, password, optional_args={'global_delay_factor': 4})
        except NetMikoTimeoutException:
            username = input('username: ')
            password = getpass('password:')
            ios = driver(ip, username, password, optional_args={'global_delay_factor': 4})
            print(colored('Time exceed!!!', 'red'))
        except SSHException:
            print(colored('Transport error with ssh or authentication', 'red'))
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
