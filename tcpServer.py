import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from threading import Thread


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        while True:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += conn.recv(8192)

            print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += conn.recv(8192)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('ImageWindow', frame)
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

        cv2.destroyAllWindows()


host = '0.0.0.0'
port = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

threads = []

while True:

    s.listen(2)

    (conn, (ip, port)) = s.accept()
    print("Connection From: " + str(ip))

    newthread = ClientThread(ip, port)

    newthread.start()

    threads.append(newthread)

    for t in threads:
        t.join()
