import threading
import queue
import main
from config import opt
from back_end.catch_package import catch_packet

net1_pretation = queue.Queue()


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
            results.extend(main.test())
            while results:
                kind = cates[results.pop(0)]
                net1_pretation.put([kind, "00" if kind != "unknown" else "01"])
