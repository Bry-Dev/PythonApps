import json
import threading as thread
import scapy.all as sc


def get_net_config():
    """
    Get json configuration file and trusted mac addresses

    Returns:
        dictionary: list of mac_address and corresponding given name
        String : IP configuration for your network with CIDR
        String : Broadcast address default is ff:ff:ff:ff:ff:ff
        String : Ethernet interface name
    """
    with open('data.json') as load_file:
        data = json.load(load_file)

    return data["mac_list"], data["ip"], data["broadcast"], data["iface"], data["router_data"]


def check_connected(ip_search: str, mac_list, mac_broad: str = "ff:ff:ff:ff:ff:ff"):
    """
    Check all devices connected on your WiFi

    Args:
        ip_search (str): IP Range. Format: ip/cidr
        mac_list (dictionary): List of Trusted MAC Addresses.
        mac_broad (str, optional): Broadcast Address. Defaults to "ff:ff:ff:ff:ff:ff".

    Returns:
        dictionary: List of unknown MAC addresses
    """
    unknown = {}
    req = sc.ARP(pdst=ip_search)
    etherpacket = sc.Ether(dst=mac_broad)
    broadcast_packet = etherpacket / req
    # or you can use this: sc.arping("ip/cidr", verbose=0)
    recv_data = sc.srp(broadcast_packet, timeout=2, verbose=False)[0]
    for sent_recv in recv_data:
        return_packet = sent_recv[1]
        if return_packet.hwsrc not in mac_list.values():
            unknown[return_packet.psrc] = return_packet.hwsrc

    return unknown


def block_mac(target_ip: str, target_mac: str, gateway_ip: str):
    """
    Completely Block a Mac Address from connecting.

    Args:
        target_ip (str): IP of target device.
        target_mac (str): MAC of target device.
        gateway_ip (str): Gateway IP or your Router.
    """
    bad_mac = "12:34:56:78:9A:BC"
    packet = sc.ARP(op=2, psrc=gateway_ip, hwsrc=bad_mac,
                    pdst=target_ip, hwdst=target_mac)
    sc.send(packet, verbose=0)


def allow_mac(target_ip: str, target_mac: str, router_ip: str, router_mac: str):
    """
    Restore connection of the blocked MAC address.

    Args:
        target_ip (str): IP of target device.
        target_mac (str): MAC address of target device.
        router_ip (str): Gateway IP.
        router_mac (str): Gateway MAC address.
    """
    packet = sc.ARP(op=2, psrc=router_ip, hwsrc=router_mac,
                    pdst=target_ip, hwdst=target_mac)
    sc.send(packet, verbose=1)


def disconnect_device(router_mac: str, target_mac: str, iface: str, count: int):
    """
    Force deauthenticate a device.

    Args:
        router_mac (str): Gateway MAC address.
        target_mac (str): MAC address of target device.
        iface (str): Ethernet Interface Name.
        count (int): Number of packets to be sent.
    """
    if count == 0:
        count = None
    dot11 = sc.Dot11(type=0, subtype=12, addr1=target_mac,
                     addr2=router_mac, addr3=router_mac)
    packet = sc.RadioTap()/dot11/sc.Dot11Deauth(reason=7)
    sc.sendp(packet, inter=0.1, count=count, iface=iface, verbose=0)


def is_int(check: int):
    """
    Check if value is int

    Args:
        check (int): value to be checked

    Returns:
        Bool: If value is int true, else false.
    """
    try:
        int(check)
        return True
    except ValueError:
        return False


def main():
    """
    Run through all connected device and ask for your confirmation if for Block or disregard.
    """
    mac_adds, ip, mac_broadcast, iface, router_data = get_net_config()
    unknown_mac = check_connected(ip, mac_adds, mac_broadcast)
    for ip, mac in unknown_mac.items():
        disconnect = input(f'Block this mac {mac}?(Y/N)')
        if disconnect.upper() == "Y":
            print("Blocking~")
            count = input("How many packets?(1 - 100) ")
            if is_int(count):
                blocking_thread = thread.Thread(
                    target=disconnect_device, name="Blocking", args=(router_data[0], mac, iface, int(count)))
                # blocking_thread.start()
            else:
                print("Not int")
                continue

        elif disconnect.upper() == "P":
            print("Poisoning~")
            poison_thread = thread.Thread(
                target=block_mac, name="Aurora", args=(ip, mac, router_data[1]))
            # poison_thread.start()
        else:
            print("Ooookay~")


if __name__ == "__main__":
    main()
