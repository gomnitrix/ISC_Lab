from identify.IdentifyThread import *
thread_list = []


def stop():
    for thread in thread_list:
        thread.stop()


def message_share():
    capture_thread = CaptureThread()
    net1_thread = Net1Thread()
    staticthread = staticThread()
    thread_list.extend([capture_thread, net1_thread,staticthread])  # TODO 加上第二个模型

    flag = True
    for thread in thread_list:
        if not flag:
           time.sleep(3)
        else:
            flag = False
        thread.start()
def get_static():
    return proto_static

def get_sum():
    val = sum(list(proto_static.values()))
    return val
def get_riskflow_num():
    return riskflow[0]
def get_rst_num():
    return rst_num[0]
if __name__ == '__main__':
    message_share()


