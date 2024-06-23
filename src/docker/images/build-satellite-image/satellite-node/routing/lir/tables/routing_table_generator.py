from routing.lir.tools import netlink_client as ncm


class RoutingTableGenerator:
    def __init__(self, path_of_routes_configuration_file: str, netlink_client: ncm.NetlinkClient):
        """
        进行 LiR 路由表的生成
        :param path_of_routes_configuration_file: 存储的路由的文件
        :param netlink_client: netlink 用户空间客户端
        """
        self.path_of_routes_configuration_file = path_of_routes_configuration_file
        self.netlink_client = netlink_client

    @classmethod
    def analyze_single_line_in_routes_configuration_file(cls, line: str, last_line: bool = False) -> str:
        """
        进行路由配置文件单行的分析
        :param last_line: 是否是最后一行
        :param line: 路由配置文件之中的一行
        """
        send_to_kernel_text = ""
        # ----------------------------- 拿到源id -----------------------------
        start_index_of_source = line.find("source:") + len("source:")
        end_index_of_source = line.find(" ", start_index_of_source)
        source_node_id = int(line[start_index_of_source:end_index_of_source])
        # ----------------------------- 拿到源id -----------------------------
        # ---------------------------- 拿到目的id -----------------------------
        start_index_of_dest = line.find("dest:") + len("dest:")
        end_index_of_dest = line.find(" ", start_index_of_dest)
        dest_node_id = int(line[start_index_of_dest: end_index_of_dest])
        # ---------------------------- 拿到目的id -----------------------------
        # ------------------------拿到目的节点的完整序列-------------------------
        identifier_and_node_sequence_in_str = (line[end_index_of_dest + 1:]).strip()
        # ------------------------拿到目的节点的完整序列-------------------------
        # ------------------------进行所有链路标识的查找-------------------------
        identifier_and_node_sequence = [int(item) for item in identifier_and_node_sequence_in_str.split("->")]
        send_to_kernel_text += f"{source_node_id},"
        send_to_kernel_text += f"{dest_node_id},"
        send_to_kernel_text += f"{int(len(identifier_and_node_sequence) / 2)},"
        for index, identifier in enumerate(identifier_and_node_sequence):
            if index != len(identifier_and_node_sequence) - 1:
                send_to_kernel_text += f"{str(identifier)},"
            else:
                send_to_kernel_text += str(identifier)
        if not last_line:
            send_to_kernel_text += "\n"
        else:
            pass
        # ------------------------进行所有链路标识的查找-------------------------
        return send_to_kernel_text

    def read_routes_and_insert_into_kernel(self):
        """
        进行 route configuration file 的解析, 分析每一个文件, 然后返回结果
        :return:
        """
        full_str = ""
        with open(self.path_of_routes_configuration_file) as f:
            all_lines = f.readlines()
        for index, line in enumerate(all_lines):
            if index == len(all_lines) - 1:
                single_line = RoutingTableGenerator.analyze_single_line_in_routes_configuration_file(line=line, last_line=True)
            else:
                single_line = RoutingTableGenerator.analyze_single_line_in_routes_configuration_file(line=line)
            full_str += single_line
        print(full_str, flush=True)
        self.netlink_client.send_netlink_data(full_str, message_type=ncm.NetlinkMessageType.CMD_INSERT_ROUTES)

    def start(self):
        print(f"-------------start generate lir routing table-------------", flush=True)
        self.read_routes_and_insert_into_kernel()
        print(f"-------------start generate lir routing table-------------", flush=True)
