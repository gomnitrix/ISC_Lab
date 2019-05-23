import numpy as np
from scapy.all import *

from utils import DBHelper as Db


def pretreatment(classes=None):
    if not classes:
        classes = [
            os.path.join("./raw/", file) for file in os.listdir("./raw/")
        ]
    helper = Db()
    conn = helper.get_con()
    for cls in classes:
        with PcapReader(cls) as reader:
            idx = 1
            file_prefix = str(cls).split("/")[-1].split(".")[0] + "_"
            for item in reader:
                if 'TCP' in item:
                    load = item['TCP']
                elif 'UDP' in item:
                    load = item['UDP']
                else:
                    load = item['IPv6']
                load = bytes(load)[:1024]
                length = len(load)
                temp = []
                for i in range(length):
                    temp.append(load[i])
                length = len(temp)
                temp.extend([0] * (1024 - length))
                formed_array = (np.array(temp, dtype='f')).reshape((1, 32, 32))
                amin, amax = formed_array.min(), formed_array.max()
                formed_array = (formed_array - amin) / (amax - amin)
                name = file_prefix + str(idx)
                helper.write_data(name, formed_array.tostring(), conn)
                idx += 1
                if idx >= 7000:
                    break


if __name__ == '__main__':
    # pretreatment(["./raw/ftp.pcapng"])
    h = Db()
    conn = h.get_con(False)
    files = h.get_files(conn)
    print(len(files))
    data = h.read_data(files[0][0], conn)
    print(data)
    print(data.shape)
