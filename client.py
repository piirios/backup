import socket
import time
import os
import json
from zipfile import ZipFile
import click
import time

TCP_IP = 'localhost' #'192.168.1.27'
TCP_PORT = 9001
BUFFER_SIZE = 1024

def reduce(liste):
    output = []
    for item in liste:
        if isinstance(liste, list): output.append(reduce(item)) 
        else: output.append(item)

def listdir_folder(path=os.path.curdir, sub=0):
    dic = []
    for element in os.listdir(path):
        p = os.path.join(path, element)
        r = None
        if os.path.isdir(p):
            try:
                r = listdir_folder(path=p, sub=sub+1)
                dic.append(r)
            except Exception as e:
                pass
        else:
            stdout = f"LIST {element}"
            print(stdout)
            dic.append(p)
    #click.echo(message=reduce(dic))
    return dic

#result = listdir_folder('/root')

def save_json(data, filename, indent=2):
    with open(filename, 'w') as f:
        r = json.dump(data, f, indent=indent)
    return


def create(path, destination_path):
    print("---start backup!---")
    filename= "backup_{}.zip".format(time.strftime("%d%m%y%H%M%S",time.localtime()))
    data = listdir_folder(path)
    def explore_write_file(zipfile, data):
        for element in data:
            stdout = f"READ {element}"
            print(stdout)
            if not isinstance(element, list):
                try:
                    zipfile.write(element)
                except Exception as e:
                    print(e)
            else:
                try:
                    explore_write_file(zipfile, element)
                except Exception as e:
                    pass
        return
    filepath = os.path.join(destination_path, filename)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    print('--- start to archivate ---')
    with ZipFile(filepath,mode="x") as zipf:
        explore_write_file(zipf, data)
        save_json(data, "backup.json")
        zipf.write("backup.json")
        os.remove("backup.json")
        print("---backup finished!---")
    return filepath

def send_backup(backup):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    pc_name = socket.gethostname().encode('utf-8')
    s.send(pc_name)
    recv = s.recv(1024)
    if recv == b'ok':
        print('header sended')
    f = open(backup, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            s.send(l)
            #print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            s.close()
            break

    print('Successfully get the file')
    s.close()
    print('connection closed')

if __name__ == '__main__':
    path = create('./hdd_louis/NSI', '.')
    send_backup(path)