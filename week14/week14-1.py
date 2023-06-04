"""
作者：Lucifer
日期：2023年06月03日
"""
from socket import *
from threading import Thread
import sys
import queue
import re
from datetime import datetime
import getpass

BS = 2048
MAXC = 48  # 可同时连接的最多客户数
name_dic = {}  # {chatter_name:connection}


class Manager:
    """
    服务器端，接收clients的消息并转播给所有/特定client
    """
    def __init__(self, port):
        self._ip = '10.192.166.53'  # 服务器端的ip地址
        self._port = port
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 端口释放后马上可以被重新使用
        self.server.bind((self._ip, self._port))
        self.server.listen(MAXC)
        self.client_list = []
        print('Welcome to 文豪野犬 chat room!')  # 聊天室主题

    def add_client(self):
        """
        获取client的连接与地址，并创建存放用户昵称的队列，多线程实现允许加入聊天室、接收消息并转播
        """
        while True:
            conn, addr = self.server.accept()
            # ci, cp = addr
            q = queue.Queue()
            t1 = Thread(target=self.permit, args=(conn, q))
            t1.start()
            t2 = Thread(target=self.speak, args=(conn, q))
            t2.start()

    def speak(self, conn, queue):
        """
        接收并转播消息，并在server界面打印每一条消息
        """
        name = queue.get()
        name_dic[name] = conn
        msg = conn.recv(BS)
        while True:
            try:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('[{}]{} : {}'.format(time, name, msg.decode('utf-8')))
                with open('manager_chatlog.txt', 'a', encoding='utf-8') as f:  # 存储manager的聊天记录
                    f.write('[{}]{} : {}'.format(time, name, msg.decode('utf-8'))+'\n')
                names = self.pick(msg.decode('utf-8'))  # 找出信息中被@的用户昵称
                if names != []:  # 判断信息中是否有被@的用户
                    names.append(name)
                    for item in names:  # 仅向被@及发送消息的人转播这条信息
                        name_dic[item].send("[{}]{} : {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                 name, msg.decode('utf-8')).encode('utf-8'))
                else:
                    for client in self.client_list:
                        client.send('[{}]{} : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                         name, msg.decode('utf-8')).encode('utf-8'))
                if msg.decode('utf-8') == 'byebye':  # 发送byebye, 表示离开聊天室
                    for client in self.client_list:
                        print('[{}]成员 {} 离开聊天室...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name))
                        client.send('[{}]成员 {} 离开聊天室...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                name).encode('utf-8'))
                        del name_dic[name]
                        self.client_list.remove(name_dic[name])
                msg = conn.recv(BS)
            except Exception as e:
                print('server error %s' % e)
                break

    def permit(self, conn, queue):
        """
        若用户发送请求，则允许进入聊天室；若发送请求以外的信息，则拒绝进入聊天室
        """
        msg = conn.recv(BS)
        if msg.decode('utf-8') == 'request':
            conn.send('Manager: accept\n'.encode('utf-8'))
            self.client_list.append(conn)
            name = conn.recv(BS)
            name = name.decode('utf-8')
            queue.put(name)
            print('Welcome {} to the chat room!'.format(name))
            for client in self.client_list:
                client.send('Welcome {} to the chat room!'.format(name).encode('utf-8'))
        else:
            conn.send('Manager: reject: please request first!\n'.encode('utf-8'))
            conn.close()

    def pick(self, message):
        """
        找出信息中所有被@的用户昵称，放入列表
        """
        regex = re.compile(r"@(" + "|".join(list(name_dic.keys())) + ")")
        names = regex.findall(message)
        return names


class Chatter:
    """
    客户端，收发消息
    """
    def __init__(self, port):
        self._ip = '10.192.166.53'
        self._port = port
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((self._ip, self._port))
        self._name = None  # 用户昵称，默认为None
        self.send_request()  # 在创建用户时就默认发送请求

    def receive(self):
        """
        接收消息并打印
        """
        while True:
            try:
                msg = self.client.recv(BS)
                if not msg:
                    break
                print(msg.decode('utf-8'))
                with open('chatter-{}_chatlog.txt'.format(self._name), 'a', encoding='utf-8') as f:
                    f.write(msg.decode('utf-8')+'\n')
                if msg.decode('utf-8') == "Manager: accept":
                    print("You are accepted to the chat room.")
                elif msg.decode('utf-8') == "Manager: reject: please request first!":
                    print("You are rejected from the chat room.")
                    break
            except Exception as e:
                print("client error %s" % e)
                break

    def send(self):
        """
        发送消息
        """
        while True:
            # 因为用户输入会被server接收并转播，最后由receive函数打印，若用input则在终端重复显示。为了美观采取getpass不显示用户输入内容
            msg = getpass.getpass("", stream=None)
            self.client.send(msg.encode('utf-8'))
            if msg == 'byebye':
                break

    def run(self):
        """
        多线程启动，收发消息
        """
        t1 = Thread(target=self.receive)
        t1.start()
        t2 = Thread(target=self.send)
        t2.start()
        t1.join()
        t2.join()

    def send_request(self):
        """
        发送进入聊天室的请求，并设置昵称
        """
        msg = 'request'
        self.client.send(msg.encode('utf-8'))
        name = input('please set your name: ')
        self._name = name
        self.client.send(name.encode('utf-8'))


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            print('usage: python week14-1.py port server|client')
        else:
            port = int(sys.argv[1])
            role = sys.argv[2]  # server, client
            if role == 'server':
                manager = Manager(port)
                ts = Thread(target=manager.add_client)
                ts.start()
                ts.join()
                print('All chatters exit...')
                manager.server.close()
            if role == 'client':
                chatter = Chatter(port)
                tc = Thread(target=chatter.run)
                tc.start()
                tc.join()
                chatter.client.close()
    except Exception as e:
        print('error %s' % e)