from scapy.all import *
import queue
from  numpy import  *
import threading
import psutil
Queue = queue.Queue()
cond = threading.Condition()

#获取网卡名称和其ip地址，不包括回环

def get_netcard():
    result =  ''
    info = psutil.net_if_addrs()
    for k,v in info.items():

        for item in v:

            if item[0] == 2 and "172" in item[1]:

                result = k

    return result

def packet_load(package):
    with cond:

        try:
            load = []
            proto = package['IP'].proto
            print(proto)
            if proto == 6:
                load = package['TCP'].payload

            elif proto == 17:
                load = package['UDP'].payload


        except IndexError:
            try:
                load = package['IPv6'].payload
            except IndexError:
                print(" ")


        if  len(load)>0:
            #print(len(load))
            int_ = [int(x) for x in bytes(load)]
            if len(int_)<1024:
                int_.extend([0] * (1024 - len(int_)))
            else :
                int_ = int_[0:1024]
            #print(int_)
            Queue.put(array(int_,dtype='f').reshape(1,32,32))
            cond.notifyAll()

def catch_packet():

        dev = get_netcard()
        sniff(iface=dev,prn=packet_load,count=0)

if __name__ == '__main__':
     t1 = threading.Thread(target = catch_packet)
     t1.start()

