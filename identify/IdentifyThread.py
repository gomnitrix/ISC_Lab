from network.main import test
from catch_package.catch_pkt import *
from catch_package.catch_pkt import packet_Queue
from network.config import opt, DefaultConfig
from .global_queue import *

proto_static = {"ssl": 0, "ssh": 0, "http": 0, "dns": 0, "ftp": 0, "mysql": 0, "unknown": 0}


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
                kind = cates[results.pop(0)]
                net1_pretation.put([kind, "00" if kind != "unknown" else "01"])


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
                item = results.pop(0)
                kind = cates[item[0]]
                tag = item[1]
                net2_pretation.put((kind, tag, "00" if kind != "unknown" else "10"))
                print(kind)


class StaticThread(BasicThread):
    def __init__(self):
        super(StaticThread, self).__init__()

    def run(self):
        while not self.if_stopped():

            while not packet_Queue.empty() and not net1_pretation.empty():
                kind = net1_pretation.get()
                pkt = packet_Queue.get()
                proto_static[kind[0]] = proto_static.get(kind[0]) + 1
