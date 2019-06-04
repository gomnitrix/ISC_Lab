from .IdentifyThread import CaptureThread, Net1Thread

thread_list = []


def stop():
    for thread in thread_list:
        thread.stop()


def message_share():
    capture_thread = CaptureThread()
    net1_thread = Net1Thread()
    thread_list.extend([capture_thread, net1_thread])  # TODO 加上第二个模型
    flag = True
    for thread in thread_list:
        if not flag:
            thread.sleep(3)
        else:
            flag = False
        thread.start()


if __name__ == '__main__':
    message_share()
