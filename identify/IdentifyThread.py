from catch_package.catch_pkt import *
from catch_package.catch_pkt import packet_Queue
from catch_package.send_rst import *
from network.config import DefaultConfig, opt
from network.main import test
from .global_queue import *

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
                item = results.pop(0)  # (data,number)
                kind = cates[item[1]]
                data = item[0]
                net1_pretation.put([data, kind, "00" if kind != "unknown" else "01"])


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
                item = results.pop(0)   # (number,("ssl",00))
                kind = cates[item[0]]
                tag = item[1]
                net2_pretation.put((tag, (kind, "00" if kind != "unknown" else "10")))
                ''' note:这里放进去的格式类似: (("ssh",00),"QQ",00)'''


class StaticThread(BasicThread):
    def __init__(self):
        super(StaticThread, self).__init__()

    def run(self):
        while not self.if_stopped():
            while not packet_Queue.empty() and not net2_pretation.empty():
                kind = net2_pretation.get()
                pkt = packet_Queue.get()
                print(kind)
                proto_static[kind[0][0]] = proto_static.get(kind[0][0]) + 1

                # test_____wait model two
                if kind[0][1] == '01' and kind[2]=='10':
                    global riskflow
                    riskflow[0] = riskflow[0] + 1
                    if pkt[0] == 6:
                        theard_send_rst(pkt)

                    # risk_flow = High_risk_traffic(proto=pkt[0],src_ip=pkt[1],dst_ip=pkt[2],
                    #                               sport=pkt[3],dport = pkt[4],load=pkt[5])
                    # risk_flow.save()
