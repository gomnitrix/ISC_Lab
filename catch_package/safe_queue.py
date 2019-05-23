import queue
from catch_package.catch_packet import *

def do():
    while True:

        #这里获取队列内容，死循环
        if not Queue.empty():
          print(Queue.get())
       # cond.wait()


def message_share():
    t1 = threading.Thread(target=catch_packet)
    t2 = threading.Thread(target=do)
    t1.start()
    t2.start()

if __name__ == '__main__':
    message_share()