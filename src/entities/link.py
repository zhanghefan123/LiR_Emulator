from enum import Enum
from src.entities import node as nm


class Link:
    class Type(Enum):
        INTER_SATELLITE_LINK = 1
        GROUND_SATELLITE_LINK = 2

        def __str__(self):
            if self.value == self.INTER_SATELLITE_LINK:
                return "INTER_SATELLITE_LINK"
            elif self.value == self.GROUND_SATELLITE_LINK:
                return "GROUND_SATELLITE_LINK"
            else:
                raise ValueError("unsupported link type")

    def __init__(self, link_id: int, link_type: Type,
                 source_node: nm.Node, source_node_interface_index: int,
                 source_node_interface_address: str, dest_node: nm.Node,
                 dest_node_interface_index: int, dest_node_interface_address: str):
        """
        链路初始化方法
        :param link_id: 链路 ID
        :param link_type:  链路类型
        :param source_node:  链路起始节点
        :param source_node_interface_index: 链路起始节点接口索引
        :param source_node_interface_address:  链路起始节点接口地址
        :param dest_node: 链路结束节点
        :param dest_node_interface_index: 链路结束节点接口索引
        :param dest_node_interface_address: 链路结束节点接口地址
        """
        self.link_id = link_id
        self.link_type = link_type
        self.source_node = source_node
        self.source_node_interface_index = source_node_interface_index
        self.source_node_interface_address = source_node_interface_address
        self.dest_node = dest_node
        self.dest_node_interface_index = dest_node_interface_index
        self.dest_node_interface_address = dest_node_interface_address
        self.linux_bridge_name = self.resolve_linux_bridge_name()

    def resolve_linux_bridge_name(self) -> str:
        """
        返回这条链路对应的 linux 网桥的名称
        :return: 这条链路对应的 linux 网桥的名称
        """
        source_node_prefix = self.source_node.node_type.get_prefix()
        dest_node_prefix = self.dest_node.node_type.get_prefix()
        return f"[br{source_node_prefix}{self.source_node.node_id}{dest_node_prefix}{self.dest_node.node_id}]"

    def __str__(self) -> str:
        """
        :return: 返回这条链路的字符串表示
        """
        return f"[link id: {self.link_id} | {self.source_node.container_name}]<-->[{self.dest_node.container_name}]"
