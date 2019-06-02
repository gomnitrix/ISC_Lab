import queue

import numpy as np
import psutil
from scapy.all import *
<<<<<<< HEAD
from catch_package.send_rst import send_rst
=======

>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389
Queue = queue.Queue()
cond = threading.Condition()


def get_netcard():
    result = ''
<<<<<<< HEAD

    info = psutil.net_if_addrs()
    for k, v in info.items():

        for item in v:

            if item[0] == 2 and "172" in item[1]:
                result = k

=======
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and "172" in item[1]:
                result = k
>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389
    return result


def packet_load(package):
    with cond:
<<<<<<< HEAD
        #print(package.show())
        try:
            load = []
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
=======

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
>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389

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
<<<<<<< HEAD
                data = (formed_array,proto,src,dst,sport,dport)
                print(data)

                Queue.put(data)
=======
                Queue.put(formed_array)

>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389
                cond.notifyAll()


def catch_packet():
    dev = get_netcard()
<<<<<<< HEAD
    sniff(iface=dev, prn=packet_load, count=0,filter="tcp")
=======
    sniff(iface=dev, prn=packet_load, count=0)
>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389


if __name__ == '__main__':
    t1 = threading.Thread(target=catch_packet)
<<<<<<< HEAD
   # t2 = threading.Thread(target=catch_packet)
    t1.start()
   # t2.start()
=======
    t1.start()
>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389
