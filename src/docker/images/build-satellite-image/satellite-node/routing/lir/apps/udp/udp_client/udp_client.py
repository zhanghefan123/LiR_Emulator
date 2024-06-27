if __name__ == "__main__":
    import sys

    sys.path.append("../../../../../")

from PyInquirer import prompt
from routing.lir.apps.types import types as tm
from routing.lir.mapper import id_to_ip_mapping_loader as itiml
from routing.lir.apps.udp import questions as qm
from routing.lir.apps.udp.udp_client import udp_ip_handler as uihm
from routing.lir.apps.udp.udp_client import udp_lir_handler as ulhm
from config import env_loader as elm


class UdpClient:
    def __init__(self):
        """
        client 初始化函数
        """
        self.selected_network_protocol = None
        self.selected_destination_port = None
        self.id_to_ip_mapping = itiml.IdToIpMappingLoader().load()
        self.env_loader = elm.EnvLoader()

    def get_user_input(self):
        """
        获取用户的输入, 包括选择的网络层协议, 目的端口等
        """
        answers_for_protocol = prompt(qm.QUESTION_FOR_PROTOCOL)["protocol"]
        if answers_for_protocol == "IP":
            self.selected_network_protocol = tm.Protocol.IP
        elif answers_for_protocol == "LIR":
            self.selected_network_protocol = tm.Protocol.LIR
        else:
            raise ValueError("不支持的网络层协议")
        answers_for_destination_port = prompt(qm.QUESTION_FOR_DESTINATION_PORT)["port"]
        self.selected_destination_port = int(answers_for_destination_port)

    def start(self):
        self.get_user_input()
        self.handle_different_network_layer()

    def handle_different_network_layer(self):
        """
        处理不同的网络层的选择
        """
        if self.selected_network_protocol == tm.Protocol.IP:
            self.handle_ip_network_protocol()
        elif self.selected_network_protocol == tm.Protocol.LIR:
            self.handle_lir_network_protocol()
        else:
            raise ValueError("不支持的网络协议")

    def handle_ip_network_protocol(self):
        """
        当用户选择了 ip 作为网络层的时候, 调用这个函数
        :return:
        """
        udp_ip_handler = uihm.UdpIpHandler(id_to_ip_mapping=self.id_to_ip_mapping,
                                           destination_port=self.selected_destination_port)
        udp_ip_handler.start()

    def handle_lir_network_protocol(self):
        """
        当用户选择了 lir 作为网络层的时候, 调用这个函数
        :return:
        """
        possible_destination_node_name_list = [item for item in self.id_to_ip_mapping.keys()]
        udp_lir_handler = ulhm.UdpLiRHandler(possible_destination_node_name_list=possible_destination_node_name_list,
                                             destination_port=self.selected_destination_port,
                                             env_loader=self.env_loader)
        udp_lir_handler.start()


if __name__ == "__main__":
    udp_client = UdpClient()
    udp_client.start()
