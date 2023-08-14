import subprocess
import re


def get_networks_and_passwords() -> list:
    command = 'netsh wlan show profile'
    networks = subprocess.check_output(command, shell=True)
    network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks.decode())

    result = []
    for network_name in network_names_list:
        command = f'netsh wlan show profile {network_name} key=clear'
        current_result = subprocess.check_output(command, shell=True).decode()
        password = re.search("(?:\s*Key Content\s*:\s)(.*)", current_result).group(1)[:-1]
        result.append(f'network:{network_name[:-1]} - password:{password}')
    return result


if __name__ == '__main__':
    for el in get_networks_and_passwords():
        print(el)