from config import env_loader as elm
from routing.lir.tools import netlink_client as ncm


class EncodingCountConfigurator:
    def __init__(self, env_loader: elm.EnvLoader, netlink_client: ncm.NetlinkClient):
        """
        初始化单次封装数量配置器
        :param env_loader: 配置加载器
        :param netlink_client: netlink 客户端
        """
        self.env_loader = env_loader
        self.netlink_client = netlink_client

    def set_encoding_count(self):
        encoding_count = self.env_loader.encoding_count
        self.netlink_client.send_netlink_data(encoding_count, ncm.NetlinkMessageType.CMD_SET_ENCODING_COUNT)

    def start(self):
        self.set_encoding_count()