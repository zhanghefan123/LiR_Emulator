from config import env_loader as elm
from routing.lir.tools import netlink_client as ncm


class BloomFilterConfigurator:
    def __init__(self, env_loader: elm.EnvLoader, netlink_client: ncm.NetlinkClient):
        """
        初始化布隆过滤器的配置器
        :param env_loader: 环境变量加载器
        :param netlink_client: netlink 的客户端
        """
        self.env_loader = env_loader
        self.netlink_client = netlink_client

    def set_default_bloom_filter(self):
        default_bloom_filter_length = self.env_loader.default_bloom_filter_length
        default_hash_seed = self.env_loader.default_hash_seed
        default_number_of_hash_funcs = self.env_loader.default_number_of_hash_funcs
        self.netlink_client.send_netlink_data(data=f"{default_bloom_filter_length},{default_hash_seed},{default_number_of_hash_funcs}",
                                              message_type=ncm.NetlinkMessageType.CMD_SET_BLOOM_FILTER_ATTRS)

    def start(self):
        self.set_default_bloom_filter()

