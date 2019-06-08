import time

from identify.IdentifyThread import CaptureThread, Net1Thread, Net2Thread, StaticThread, proto_static


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


def get_static():
    return proto_static


ident = Identify()

if __name__ == '__main__':
    ident.message_share()
