import functools
from typing import List
from routing.lir.tools import netlink_client as ncm


class RoutesLoader:
    def __init__(self, all_routes_file_path="/configuration/lir/routes"):
        """
        初始化路由加载器
        :param all_routes_file_path: 每两个节点间的路由存储文件
        """
        self.all_routes_file_path = all_routes_file_path
        self.netlink_client = ncm.NetlinkClient()
        self.routes = {}

    def load_lir_routes(self):
        """
        从 all_route_file 加载路由并存储到 routes 之中
        """
        with open(self.all_routes_file_path) as f:
            all_route_strs = f.readlines()
        for route_str in all_route_strs:
            self.analyze_single_lir_route(route_str=route_str)

    def analyze_single_lir_route(self, route_str: str):
        """
        分析单行 lir 路由
        :param route_str 单个路由字符串
        """
        # ----------------------------- 拿到源id -----------------------------
        start_index_of_source = route_str.find("source:") + len("source")
        end_index_of_source = route_str.find(" ", start_index_of_source)
        source_node_id = int(route_str[start_index_of_source:end_index_of_source])
        # ----------------------------- 拿到源id -----------------------------
        # ---------------------------- 拿到目的id ----------------------------
        start_index_of_dest = route_str.find("dest:") + len("dest:")
        end_index_of_dest = route_str.find(" ", start_index_of_dest)
        dest_node_id = int(route_str[start_index_of_dest: end_index_of_dest])
        # ---------------------------- 拿到目的id ----------------------------
        # ------------------------拿到目的节点的完整序列-------------------------
        identifier_and_node_sequence_in_str = (route_str[end_index_of_dest + 1:]).strip()
        # ------------------------拿到目的节点的完整序列-------------------------
        self.routes[(source_node_id, dest_node_id)] = identifier_and_node_sequence_in_str

    def insert_route(self, source: int, dest: int):
        """
        进行路由的插入
        :param source: 源节点
        :param dest: 目的节点
        """
        link_and_node_identifiers = self.routes[(source, dest)]
        link_and_node_identifiers_str = ""
        for index, link_or_node_identifier in enumerate(link_and_node_identifiers):
            if index != len(link_and_node_identifiers) - 1:
                link_and_node_identifiers_str += str(link_or_node_identifier) + ","
            else:
                link_and_node_identifiers_str += str(link_or_node_identifier)
        send_to_kernel_str = f"{source},{dest},{len(link_and_node_identifiers) / 2},{link_and_node_identifiers_str}"
        self.netlink_client.send_netlink_data(data=send_to_kernel_str,
                                              message_type=ncm.NetlinkMessageType.CMD_INSERT_ROUTES)

    def insert_multicast_route(self, destination_list: List[int]):
        """
        进行多播相关的路由的插入 [假设目的节点是 B,C,D, 源节点是 A], 那么我们需要插入
        A->B(在内核之中已经存在了, 因为所有的单播路由条目已经插入了) B->C B->D 其中 B 是主节点
        :param destination_list: 目的节点 B,C,D
        :return:
        """
        primary_node = destination_list[0]  # dest list 的第一个将充当主节点
        for index in range(1, len(destination_list)):
            destination_node = destination_list[index]
            self.insert_route(source=primary_node, dest=destination_node)

    def __str__(self):
        """
        返回字符串表示
        """
        str_list = [f"{source_dest_pair}:{self.routes[source_dest_pair]}" for source_dest_pair in self.routes.keys()]
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", str_list, "")
