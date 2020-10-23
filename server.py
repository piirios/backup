import socket
from threading import Thread
import os
import time

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


class ClientThread(Thread):

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        pc_name = self.sock.recv(1024).decode('utf-8')
        self.sock.send(b'ok')
        if not os.path.exists(os.path.join(os.curdir, pc_name)):
            os.makedirs(f'./{pc_name}')
        name = f"{pc_name}/{time.time()}.zip"
        with open(name, 'wb') as f:
            print('file opened')
            while True:
                #print('receiving data...')
                data = self.sock.recv(BUFFER_SIZE)
                print('data=%s', (data))
                if not data:
                    f.close()
                    print('file close()')
                    break
                # write data to a file
                f.write(data)



tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = tcpsock.accept()
    print('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()