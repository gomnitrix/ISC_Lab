import time

from identify.IdentifyThread import CaptureThread, Net1Thread, Net2Thread, StaticThread, proto_static, riskflow, rst_num,app_static


class Identify:
    def __init__(self):
        self.thread_list = []

    def stop(self):
        for thread in self.thread_list:
            thread.stop()

    def message_share(self):
        capture_thread = CaptureThread()
        net1_thread = Net1Thread()
        net2_thread = Net2Thread()
        staticthread = StaticThread()
        self.thread_list.extend([capture_thread, net1_thread, net2_thread, staticthread])

        flag = True
        for thread in self.thread_list:
            if not flag:
                time.sleep(3)
            else:
                flag = False
            thread.start()


def get_proto_static():
    return proto_static

def get_app_num():
    return app_static



def get_sum():
    val = sum(list(proto_static.values()))
    return val


def get_riskflow_num():
    return riskflow[0]


def get_rst_num():
    return rst_num[0]

ident = Identify()

if __name__ == '__main__':
    ident.message_share()
