

from catch_package.setiptable import enable,reset
from identify.IdentifyThread import *
from utils.DbHelper import read

id = [0]


class Identify:
    def __init__(self):
        self.thread_list = []

    def stop(self):
        for thread in self.thread_list:
            thread.stop()

    def message_share(self):
        capture_thread = CaptureThread()
        handle_thread = HandleThread()
        net1_thread = Net1Thread()
        net2_thread = Net2Thread()
        staticthread = StaticThread()
        self.thread_list = []
        self.thread_list.extend([capture_thread, handle_thread, net1_thread, net2_thread, staticthread])

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


def get_block_num():
    return block[0]


def get_rst_num():
    return rst_num[0]



def get_riskflow_retail():
    values = read(id[0])
    print(values)
    print(id[0])
    length = len(values)
    if length > 0:
        id[0] = values[length - 1]['id']
    return values

def get_filter():
    values = read_ft()
    return values

def iptable_enable():
    enable()

def iptable_reset():
    reset()


ident = Identify()

if __name__ == '__main__':
    ident.message_share()
