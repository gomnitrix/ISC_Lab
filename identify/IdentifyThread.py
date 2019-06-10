from catch_package.catch_pkt import catch_packet,handle_packages
from catch_package.catch_pkt import packet_Queue
from catch_package.send_rst import *
from catch_package.setiptable import *
from network.config import DefaultConfig, opt
from network.main import test
from network.utils import DbHelper
from .global_queue import *
lock = Lock()
proto_static = {"ssl": 0, "ssh": 0, "http": 0, "dns": 0, "ftp": 0, "mysql": 0, "unknown": 0}

app_static = {"QQ": 0, "WeChat": 0, "iqy": 0, "Thunder": 0, "NetEase": 0,"unknown": 0 }
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


class HandleThread(BasicThread):
    def __init__(self):
        super(HandleThread, self).__init__()

    def run(self):
        while not self.if_stopped():
            handle_packages()


class Net1Thread(BasicThread):
    def __init__(self):
        super(Net1Thread, self).__init__()

    def run(self):
        results = []
        cates = {val: key for key, val in opt.classes_dict.items()}
        cates[len(opt.classes_dict)] = "unknown"
        uq_opt = DefaultConfig()
        while not self.if_stopped():
            results.extend(test(uq_opt=uq_opt, load_model_path=opt.net1_model))
            while results:
                kind = cates[results.pop(0)]
                net1_pretation.put((kind, "00" if kind != "unknown" else "01"))


class Net2Thread(BasicThread):
    def __init__(self):
        super(Net2Thread, self).__init__()

    def run(self):
        results = []
        cates = {val: key for key, val in opt.app_dict.items()}
        cates[len(opt.app_dict)] = "unknown"
        uq_opt = DefaultConfig()
        while not self.if_stopped():
            results.extend(test(uq_opt=uq_opt, load_model_path=opt.net2_model, model="EncIdentNet"))
            while results:

                if net1_pretation.empty():
                    time.sleep(0.5)
                    continue
                kind = cates[results.pop(0)]
                tag = net1_pretation.get()
                net2_pretation.put((tag, (kind, "00" if kind != "unknown" else "10")))
                ''' note:这里放进去的格式类似: (("ssh",00),("QQ",00))'''


class StaticThread(BasicThread):
    def __init__(self):
        super(StaticThread, self).__init__()

    def run(self):



        while not self.if_stopped():
            while not packet_Queue.empty() and not net2_pretation.empty():
                kind = net2_pretation.get()
                pkt = packet_Queue.get()
                proto_static[kind[0][0]] = proto_static.get(kind[0][0]) + 1
                app_static[kind[1][0]] = app_static.get(kind[1][0])+1
                if kind[0][1] == '01' and kind[1][1] == '10':

                    riskflow[0] = riskflow[0] + 1
                    if pkt[0] == 6:
                        theard_send_rst(pkt)
                    else:
                        if "172" in pkt[1]:
                            deny_ip(pkt[2])
                        else:
                            deny_ip(pkt[1])
                    DbHelper.theard_write(proto=pkt[0],src_ip=pkt[1],dst_ip=pkt[2],sport=int(pkt[3]),dport = int(pkt[4]))


