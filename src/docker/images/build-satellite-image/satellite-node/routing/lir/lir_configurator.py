from config import env_loader as elm
from routing.lir.tables import interface_table_generator as itgm
from routing.lir.tables import routing_table_generator as rtgm
from routing.lir.tools import netlink_client as ncm
from routing.lir.mapper import net_to_id_mapper as ntimm
from routing.lir.bloom import bloom_filter_configurator as bfcm
from routing.lir.policy import encoding_count_configurator as eccm


class LiRConfigurator:
    def __init__(self, env_loader: elm.EnvLoader):
        """
        进行 lir 配置器的初始化
        :param env_loader: 环境变量管理器
        """
        self.lir_enabled = env_loader.lir_enabled
        self.container_name = env_loader.container_name
        self.has_validation_method_or_not = env_loader.has_validation_method_or_not
        self.netlink_client = ncm.NetlinkClient()
        self.interface_table_generator = itgm.InterfaceTableGenerator(
            path_of_name_to_lid_file=f"/configuration/lir/identifiers/{self.container_name}.conf",
            netlink_client=self.netlink_client)
        self.routing_table_generator = rtgm.RoutingTableGenerator(
            path_of_routes_configuration_file=f"/configuration/lir/routes/{self.container_name}.conf",
            netlink_client=self.netlink_client
        )
        self.net_to_id_mapper = ntimm.NetNamespaceToNodeIdMapper(netlink_client=self.netlink_client,
                                                                 node_id=env_loader.node_id)
        self.bloom_filter_configurator = bfcm.BloomFilterConfigurator(env_loader=env_loader,
                                                                      netlink_client=self.netlink_client)
        self.encoding_count_configurator = eccm.EncodingCountConfigurator(env_loader=env_loader,
                                                                          netlink_client=self.netlink_client)

    def config_lir(self):
        """
        通过 netlink 向内核传递 lir 所需要的配置
        :return:
        """
        if self.lir_enabled:
            if not self.has_validation_method_or_not:
                self.encoding_count_configurator.start()
            else:
                pass
            self.bloom_filter_configurator.start()  # 注意一开始就要进行布隆过滤器的配置
            self.interface_table_generator.start()
            self.routing_table_generator.start()
            self.net_to_id_mapper.start()
        else:
            pass
