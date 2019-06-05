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
                    load = item['TCP'].payload
                elif 'UDP' in item:
                    load = item['UDP'].payload
                else:
                    load = item['IPv6'].payload
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
                    helper.write_data(name, formed_array.tostring(), conn)
                    idx += 1
                if idx >= 15000:
                    break


if __name__ == '__main__':
    pretreatment(["./raw/mysql.pcapng"])
    h = Db()
    conn = h.get_con(False)
    files = h.get_files(conn)
    print(len(files))
    data = h.read_data(files[0][0], conn)
    conn.close()
    print(data)
    print(data.shape)
