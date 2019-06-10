import os
from utils.DbHelper import *
#ufw 防火墙 禁止ip访问
def deny_ip(ip):
    command = "ufw deny from "+ip
    theard_write_bl(ip)
    os.system(command)

def enable():
    os.system("ufw enable")

#重置规则
def reset():
    os.system("ufw reset")



if __name__ == '__main__':
   deny_ip("123.0.0.1")
   deny_ip("123.0.0.1")
   deny_ip("123.3.0.1")
