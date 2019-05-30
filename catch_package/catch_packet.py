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
            load = []
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
            int_ = [int(x) for x in bytes(load)]
            if len(int_) < 1024:
                int_.extend([0] * (1024 - len(int_)))
            else:
                int_ = int_[0:1024]
            img = np.array(int_, dtype='f').reshape((1, 32, 32))
            if img.any():
                amin, amax = img.min(), img.max()
                formed_array = (img - amin) / (amax - amin)
                Queue.put(formed_array)

                cond.notifyAll()


def catch_packet():
    dev = get_netcard()
    sniff(iface=dev, prn=packet_load, count=0)


if __name__ == '__main__':
    t1 = threading.Thread(target=catch_packet)
    t1.start()
