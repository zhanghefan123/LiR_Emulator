if __name__ == "__main__":
    import sys

    sys.path.append("../../../../../")

import socket
from PyInquirer import prompt
from routing.lir.apps.udp import questions as qm
from loguru import logger


class UdpServer:
    def __init__(self):
        """
        初始化函数
        """
        self.listening_port = None
        self.selected_listening_port = None
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_user_input(self):
        """
        获取用户输入
        """
        answers_for_port = prompt(qm.QUESTION_FOR_SERVER_LISTEN_PORT)
        self.selected_listening_port = int(answers_for_port["port"])

    def bind_ip_port_and_receive_data(self):
        """
        绑定 ip 端口，并准备进行数据的接收
        """
        all_interface_address = "0.0.0.0"
        self.udp_socket.bind((all_interface_address, self.selected_listening_port))
        while True:
            data, address = self.udp_socket.recvfrom(1024)
            data = data.decode()
            if data == "exit":
                break
            else:
                logger.success(data)

    def start(self):
        """
        启动服务器端
        """
        self.get_user_input()
        self.bind_ip_port_and_receive_data()
        logger.success("服务器端退出!")


if __name__ == "__main__":
    udp_server = UdpServer()
    udp_server.start()
