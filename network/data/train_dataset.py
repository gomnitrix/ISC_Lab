import numpy as np
from scapy.all import *

from utils import DBHelper as Db


def pretreatment(classes=None):
    if not classes:
        classes = [
            os.path.join("./raw/app/", file) for file in os.listdir("./raw/app/")
        ]
    helper = Db()
    conn = helper.get_con()
    for cls in classes:
        with PcapReader(cls) as reader:
            idx = 18000
            file_prefix = str(cls).split("/")[-1].split(".")[0] + "_"
            label = file_prefix.strip('_')
            for item in reader:
                if 'TCP' in item:
                    load = item['TCP'].payload
                elif 'UDP' in item:
                    load = item['UDP'].payload
                elif 'IPv6' in item:
                    load = item['IPv6'].payload
                else:
                    continue
                load = bytes(load)[:1024]
                if not load:
                    continue
                length = len(load)
                temp = [load[i] for i in range(length)]
                temp.extend([0] * (1024 - length))
                formed_array = np.array(temp, dtype='f').reshape((1, 32, 32))
                if formed_array.any():
                    amin, amax = formed_array.min(), formed_array.max()
                    formed_array = (formed_array - amin) / (amax - amin)
                    if np.any(np.isnan(formed_array)):
                        continue
                    name = file_prefix + str(idx)
                    helper.write_data(name, formed_array.tostring(), label, conn)
                    idx += 1
                if idx >= 23000:
                    break


if __name__ == '__main__':
    pretreatment(["./raw/app/Thunder.pcapng"])
    h = Db()
    conn = h.get_con(False)
    files = h.get_files(conn)
    print(len(files))
    data = h.read_data(files[0][0], conn)
    conn.close()
    print(data)
    print(data[0].shape)
