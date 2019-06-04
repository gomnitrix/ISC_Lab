import queue

import numpy as np
import psutil
from scapy.all import *

Queue = queue.Queue()
cond = threading.Condition()


def get_netcard():
    result = ''
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and "172" in item[1]:
                result = k
    return result


def packet_load(package):
    with cond:

        try:
            proto = package['IP'].proto
            if proto == 6:
                load = package['TCP'].payload

            elif proto == 17:
                load = package['UDP'].payload

        except IndexError:
            try:
                load = package['IPv6'].payload
            except IndexError:
                print(" ")

        if len(load) > 0:
            load = bytes(load)[:1024]
            length = len(load)
            temp = [load[i] for i in range(length)]
            temp.extend([0] * (1024 - length))
            img = np.array(temp, dtype='f').reshape((1, 32, 32))
            if img.any():
                amin, amax = img.min(), img.max()
                formed_array = (img - amin) / (amax - amin)
                Queue.put(formed_array)
                cond.notifyAll()


def catch_packet():
    dev = get_netcard()
    sniff(iface=dev, prn=packet_load, count=0)


def test():
    classes = "C:/Users/omnitrix/PycharmProjects/IC_Secu/network/data/raw/httptest2.pcapng"
    with PcapReader(classes) as reader:
        for item in reader:
            if 'TCP' in item:
                load = item['TCP']
            elif 'UDP' in item:
                load = item['UDP']
            else:
                load = item['IPv6']
            load = bytes(load)[:1024]
            length = len(load)
            temp = []
            for i in range(length):
                temp.append(load[i])
            length = len(temp)
            temp.extend([0] * (1024 - length))
            formed_array = (np.array(temp, dtype='f')).reshape((1, 32, 32))
            amin, amax = formed_array.min(), formed_array.max()
            formed_array = (formed_array - amin) / (amax - amin)
            Queue.put(formed_array)


if __name__ == '__main__':
    t1 = threading.Thread(target=catch_packet)
    t1.start()
