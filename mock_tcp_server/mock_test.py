import sys
import socket

class TcpServer:
    def __init__(self,_ip,_port):
        self.recv_addr = (_ip, _port)
        self.buffersize = 10240000
        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.bind(self.recv_addr)
        self.comm_socket.listen(10)

    def send(self,string_data,addr):
        self.client_socket.send(string_data)

    def recv(self):
        self.client_sock,self.recv_from_addr = self.comm_socket.accept()
        self.client_socket = self.client_sock
        self.string_data = self.client_sock.recv(self.buffersize)
        return (self.string_data,self.recv_from_addr)

    def __del__(self):
        self.comm_socket.close()
        self.client_socket.close()

def mock():
    _tcp = TcpServer("0.0.0.0",8866)
    while True:
        _tcp.recv_data,_tcp.recv_addr = _tcp.recv()
        print("recv from:",_tcp.recv_addr)
        _tcp.send_data = "helloworld"
        _tcp.send(_tcp.send_data, _tcp.recv_addr)
        print("send over!")


if __name__ == '__main__':
    mock()