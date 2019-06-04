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
            src = package['IP'].src
            dst = package['IP'].dst
            sport = ''
            dport = ''
            if proto == 6:
                load = package['TCP'].payload
                sport = package['TCP'].sport
                dport = package['TCP'].dport
            elif proto == 17:
                load = package['UDP'].payload
                sport = package['UDP'].sport
                dport = package['UDP'].dport

        except IndexError:
            # try:
            #     load = package['IPv6'].payload
            #     # src = package['IPv6'].src
            #     # dst = package['IPv6'].dst
            # except IndexError:
            return

        if len(load) > 0:
            load = bytes(load)[:1024]
            length = len(load)
            temp = [load[i] for i in range(length)]
            temp.extend([0] * (1024 - length))
            img = np.array(temp, dtype='f').reshape((1, 32, 32))
            if img.any():
                amin, amax = img.min(), img.max()
                formed_array = (img - amin) / (amax - amin)
                if not np.any(np.isnan(formed_array)):
                    data = (formed_array, proto, src, dst, sport, dport)
                    Queue.put(data)
                    cond.notifyAll()


def catch_packet(count):
    dev = get_netcard()

    sniff(iface=dev, prn=packet_load, count=count, filter="tcp")


if __name__ == '__main__':
    t1 = threading.Thread(target=catch_packet)
    t1.start()
