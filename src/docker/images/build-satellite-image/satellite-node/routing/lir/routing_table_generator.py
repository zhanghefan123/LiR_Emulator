from routing.lir import netlink_client as ncm


class RoutingTableGenerator:
    def __init__(self, path_of_routes_configuration_file: str, netlink_client: ncm.NetlinkClient):
        """
        进行 LiR 路由表的生成
        :param path_of_routes_configuration_file: 存储的路由的文件
        :param netlink_client: netlink 用户空间客户端
        """
        self.path_of_routes_configuration_file = path_of_routes_configuration_file
        self.netlink_client = netlink_client

    def read_routes_and_insert_into_kernel(self):
        full_str = ""
        with open(self.path_of_routes_configuration_file) as f:
            all_lines = f.readlines()
        for line in all_lines:
            print(line)

    def start(self):
        self.read_routes_and_insert_into_kernel()
