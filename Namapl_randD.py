from pprint import pprint
from napalm import get_network_driver
from getpass import getpass
from netmiko import NetMikoAuthenticationException
import json


username = input('username')
password = getpass('password')
driver = get_network_driver('ios')

with open('mydevices.txt','r') as router_db:
    for router in router_db:
    #set up to connect to a switch from switch_db
        try:
            device = driver(router, username, password)
            device.open()
        except NetMikoAuthenticationException:
            print('Authentication Error!')
            username = input('username')
            password = getpass('password')
            device = driver(router, username, password)
            device.open()
        else:
            print('line after try block')
            pprint(device.get_interfaces())
            device.close()
            print('switch is closed')


