import queue
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import psutil
from scapy.all import *

from catch_package.setiptable import *
from network.config import opt

net1_datas = queue.Queue()
net2_datas = queue.Queue()
packet_Queue = queue.Queue()
raw_package_queue = queue.Queue()
cond = threading.Condition()
FLT = []
FLT_result = []
lock = Lock()


def get_netcard():
    result = ''
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and "172" in item[1]:
                result = k

    return result


def packet_load(package):
    load = ''
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

            length = len(FLT)
            if length != 0 and load.__contains__(FLT[length - 1]):
                FLT_result.append(proto, src, dst, sport, dport)
                # if  "172" in src:
                #     deny_ip(dst)
                # else:
                #     deny_ip(src)
            load = bytes(load)[:1024]
            length = len(load)
            int_ = [load[i] for i in range(length)]
            int_.extend([0] * (1024 - length))
            img = np.array(int_, dtype='f').reshape((1, 32, 32))
            if img.any():
                amin, amax = img.min(), img.max()
                formed_array = (img - amin) / (amax - amin)
                data = (proto, src, dst, sport, dport, load)
                lock.acquire()
                net1_datas.put(formed_array)
                net2_datas.put(formed_array)
                packet_Queue.put(data)
                lock.release()
                cond.notifyAll()


def put_packet(package):
    raw_package_queue.put(package)


def handle_packages():
    with ThreadPoolExecutor(max_workers=opt.num_workers) as executor:
        while not raw_package_queue.empty():
            package = raw_package_queue.get()
            executor.submit(packet_load, package)


def catch_packet(num):
    dev = get_netcard()
    sniff(iface=dev, prn=packet_load, count=num)
