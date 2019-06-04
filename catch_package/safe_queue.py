from catch_package.catch_packet import *
from network import main
from network.config import opt


def forecast():
    results = []
    pretation = []
    cates = {val: key for key, val in opt.classes_dict.items()}
    cates[opt.cates] = "unknow"
    for i in range(5):
        results.extend(main.test())
    while results:
        pretation.append(cates[results.pop(0)])
    print(pretation)
    print(len(pretation))
    print("http: " + str(pretation.count("http")))
    print("unknow: " + str(pretation.count("unknow")))
    print("ssl: " + str(pretation.count("ssl")))


def message_share():
    t1 = threading.Thread(target=catch_packet)
    t2 = threading.Thread(target=forecast)
    t1.start()
    time.sleep(2)
    t2.start()


if __name__ == '__main__':
    # message_share()
    t1 = threading.Thread(target=test)
    t2 = threading.Thread(target=forecast)
    t1.start()
    time.sleep(1)
    t2.start()
