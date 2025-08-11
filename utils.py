
import netifaces

def get_ip_address() -> str:
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue  # пропускаем loopback интерфейс
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                if 'addr' in link:
                    return link['addr']
    return '127.0.0.1'


    