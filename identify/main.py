from identify.IdentifyThread import *
import _thread
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


if __name__ == '__main__':
    message_share()


