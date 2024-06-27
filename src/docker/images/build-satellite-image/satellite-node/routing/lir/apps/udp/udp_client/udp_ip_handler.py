import socket
from typing import Dict, List
from PyInquirer import prompt
from routing.lir.apps.udp import questions as qm
from loguru import logger


class UdpIpHandler:
    def __init__(self, id_to_ip_mapping: Dict[str, List[str]], destination_port: int):
        """
        初始化选用 ip 作为网络层，上层为 udp 的处理器
        :param id_to_ip_mapping: 从 id 到 ip 的映射
        :param destination_port: 目的端口
        """
        self.id_to_ip_mapping = id_to_ip_mapping
        self.destination_port = destination_port

    def select_destination_node(self) -> str:
        """
        让用户选择目的节点 id, 然后通过 id_to_ip_mapping, 选择到对应的 ip
        :return: 选择的节点的名称
        """
        question_for_destination_node = qm.QUESTION_FOR_DESTINATION
        question_for_destination_node[0]["choices"] = list(self.id_to_ip_mapping.keys())
        selected_destination_node = prompt(question_for_destination_node)["destination"]
        return selected_destination_node

    def send_data(self, udp_socket: socket.socket, destination_ip_address: str):
        """
        进行消息的发送
        """
        while True:
            message = input("请输入您想要发送的消息: (exit to break)")
            if message == "exit":
                udp_socket.sendto(message.encode(), (destination_ip_address, self.destination_port))
                break
            else:
                udp_socket.sendto(message.encode(), (destination_ip_address, self.destination_port))

    @classmethod
    def create_udp_socket(cls):
        """
        进行 socket 的创建
        """
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return udp_socket

    def start(self):
        selected_destination_node = self.select_destination_node()
        selected_destination_ip = self.id_to_ip_mapping[selected_destination_node][0]
        udp_socket = self.create_udp_socket()
        self.send_data(udp_socket=udp_socket, destination_ip_address=selected_destination_ip)
        logger.success("udp 客户端退出")
