import os
import socket
from typing import List
from PyInquirer import prompt
from routing.lir.apps.udp import questions as qm
from config import env_loader as elm
from routing.lir.apps.types import types as tm
from routing.lir.tables import routes_loader as rlm
import time

class UdpLiRHandler:
    def __init__(self, possible_destination_node_name_list: List[str],
                 destination_port: int,
                 env_loader: elm.EnvLoader,
                 routes_loader: rlm.RoutesLoader):
        """
        :param possible_destination_node_name_list: 可以选择的目的节点的名称列表
        :param destination_port: 目的端口
        :param env_loader: 环境变量加载器
        :param routes_loader: 路由条目加载器
        """
        self.possible_destination_node_name_list = possible_destination_node_name_list
        self.destination_port = destination_port
        self.env_loader = env_loader
        self.transmission_pattern = None
        self.routes_loader = routes_loader

    def get_user_input(self):
        """
        获取用户输入
        """
        answers_for_transmission_pattern = prompt(qm.QUESTION_FOR_LIR_TRANSMISSION_PATTERN)["transmission_pattern"]
        if answers_for_transmission_pattern == "unicast":
            self.transmission_pattern = tm.TransmissionPattern.UNICAST
        elif answers_for_transmission_pattern == "multicast":
            self.transmission_pattern = tm.TransmissionPattern.MULTICAST
        else:
            raise ValueError("不支持的传输模式")

    def select_destination_node(self) -> int:
        """
        让用户选择目的节点 id, 然后通过 id_to_ip_mapping, 选择到对应的 ip
        :return: 选择的节点的名称
        """
        question_for_destination_node = qm.QUESTION_FOR_DESTINATION
        question_for_destination_node[0]["choices"] = self.possible_destination_node_name_list
        selected_destination_node_str = prompt(question_for_destination_node)["destination"]
        # 将节点id提取出来
        selected_destination_node_id = int(
            selected_destination_node_str[selected_destination_node_str.find("satellite") + len("satellite"):])
        return selected_destination_node_id

    def select_destination_node_ids(self) -> List[int]:
        """
        对于多播情况，我们应该选择多个节点
        :return:
        """
        number_of_destinations = int(prompt(qm.QUESTION_FOR_NUMBER_OF_DESTINATIONS)["count"])
        destination_node_list = []
        for index in range(number_of_destinations):
            selected_destination_node_id = self.select_destination_node()
            destination_node_list.append(selected_destination_node_id)
        return destination_node_list

    @classmethod
    def create_udp_socket_and_set_sock_option(cls, destination_node_list):
        """
        创建 socket 并设置好选项
        :return:
        """
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        number_of_destinations = len(destination_node_list)
        first_eight_bytes = [0x94, 0x28] + [int(os.getenv("NODE_ID"))] + [
            number_of_destinations] + destination_node_list + [0x0] * (8 - 4 - number_of_destinations)
        remained_thirty_two_bytes = [0x0] * 32
        byte_array = bytearray(first_eight_bytes + remained_thirty_two_bytes)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_DEBUG, 1)
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_OPTIONS, byte_array)
        return udp_socket

    def handle_different_transmission_pattern(self):
        """
        进行不同的传输协议的处理
        :return:
        """
        if self.transmission_pattern == tm.TransmissionPattern.UNICAST:
            self.handle_unicast_transmission_pattern()
        elif self.transmission_pattern == tm.TransmissionPattern.MULTICAST:
            self.handle_multicast_transmission_pattern()
        else:
            raise ValueError("不支持的传输模式")

    def handle_unicast_transmission_pattern(self):
        """
        处理单播协议
        :return:
        """
        # 选择单个卫星
        selected_destination_node_id = self.select_destination_node()
        # 创建好单播 socket
        unicast_udp_socket = self.create_udp_socket_and_set_sock_option([selected_destination_node_id])
        # 进行消息的发送
        self.send_data(unicast_udp_socket, [selected_destination_node_id] * 4)

    def handle_multicast_transmission_pattern(self):
        """
        处理多播协议
        :return:
        """
        # 选择一系列的目的节点
        destination_node_list = self.select_destination_node_ids()  # 进行多个目的节点的选择
        # 创建好多播 socket
        multicast_udp_socket = self.create_udp_socket_and_set_sock_option(destination_node_list)
        if len(destination_node_list) != 4:
            # 少于 4 个的部分使用 250 进行填充
            destination_node_list = destination_node_list + [250] * (4 - len(destination_node_list))
        self.send_data(multicast_udp_socket, destination_node_list)

    def send_data(self, udp_socket: socket.socket, destination_node_id_list: List[int]):
        """
        进行数据的发送
        :param udp_socket: 创建的带有 lir option 的 udp_socket
        :param destination_node_id_list: 目的节点id的列表
        :return:
        """
        destination_node_ids_in_str = [str(item) for item in destination_node_id_list]
        lir_destination_address = ".".join(destination_node_ids_in_str)
        while True:
            send_message = ("f" * 100).encode()
            msg_count = int(prompt(qm.QUESTION_FOR_MESSAGE_COUNT)["count"])
            interval = float(prompt(qm.QUESTION_FOR_INTERVAL)["interval"])
            for index in range(msg_count):
                udp_socket.sendto(send_message, (lir_destination_address, self.destination_port))
                time.sleep(interval)
            continue_or_not = prompt(qm.QUESTION_FOR_CONTINUE)["continue"]
            if continue_or_not == "yes":
                pass
            else:
                break

    def start(self):
        self.get_user_input()
        self.handle_different_transmission_pattern()
