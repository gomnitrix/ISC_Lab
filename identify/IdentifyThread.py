import threading
import queue

from network.config import opt
from catch_package.send_rst import *
from catch_package.catch_pkt import *
from network.main import *
from catch_package.catch_pkt import packet_Queue
from traffic_recognition.models import High_risk_traffic
net1_pretation = queue.Queue()
proto_static = {"ssl": 0, "ssh": 0, "http": 0, "dns": 0, "ftp": 0, "mysql": 0,"unknown":0}
app_static = {"QQ":0,"wechat":0,"wangyi":0,"thrunder":0}
riskflow = [0]
class BasicThread(threading.Thread):
    def __init__(self):
        super(BasicThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def if_stopped(self):
        return self._stop_event.is_set()


class CaptureThread(BasicThread):
    def __init__(self):
        super(CaptureThread, self).__init__()

    def run(self):
        while not self.if_stopped():
            catch_packet(opt.capture_num)


class Net1Thread(BasicThread):
    def __init__(self):
        super(Net1Thread, self).__init__()

    def run(self):
        results = []
        cates = {val: key for key, val in opt.classes_dict.items()}
        cates[opt.cates] = "unknown"

        while not self.if_stopped():
            tt  = test()

            results.extend(tt)
            while results:
                kind = cates[results.pop(0)]

                net1_pretation.put([kind, "00" if kind != "unknown" else "01"])


class staticThread(BasicThread):
    def __init__(self):
        super(staticThread, self).__init__()

    def run(self):
        while not self.if_stopped():

            while not packet_Queue.empty() and not net1_pretation.empty():
                kind = net1_pretation.get()
                pkt = packet_Queue.get()
                proto_static[kind[0]] = proto_static.get(kind[0])+1
                #test_____wait model two
                if kind[1]=='01':
                    global riskflow
                    riskflow[0] = riskflow[0]+1
                    if pkt[0] == 6:
                        theard_send_rst(pkt)

                    # risk_flow = High_risk_traffic(proto=pkt[0],src_ip=pkt[1],dst_ip=pkt[2],
                    #                               sport=pkt[3],dport = pkt[4],load=pkt[5])
                    # risk_flow.save()

if __name__ == '__main__':
    net1 = Net1Thread()
    Net1Thread.start()