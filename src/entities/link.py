from enum import Enum
from src.entities import node as nm
from pyroute2 import IPRoute, NetNS


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
        self.source_node_interface_id = source_node_interface_index + 1
        self.source_node_interface_address = source_node_interface_address
        self.dest_node = dest_node
        self.dest_node_interface_index = dest_node_interface_index
        self.dest_node_interface_id = dest_node_interface_index + 1
        self.dest_node_interface_address = dest_node_interface_address
        self.linux_bridge_name = self.resolve_linux_bridge_name()

    def get_source_and_dest_veth_names(self) -> (str, str):
        """
        获取这条链路源节点的源头节点和目的节点的名称
        :return: 源节点的 veth 的名称, 目的节点的 veth 的名称
        """
        source_node_prefix = self.source_node.node_type.get_prefix()
        source_node_id = self.source_node.node_id
        source_node_veth_name = f"{source_node_prefix}{source_node_id}_index{self.source_node_interface_id}"
        dest_node_prefix = self.dest_node.node_type.get_prefix()
        dest_node_id = self.dest_node.node_id
        dest_node_veth_name = f"{dest_node_prefix}{dest_node_id}_index{self.dest_node_interface_id}"
        return source_node_veth_name, dest_node_veth_name

    def get_source_and_dest_net_namespace_path(self) -> (str, str):
        """
        获取这条链路的源节点和目的节点的网络命名空间的路径
        :return: 源节点的网络命名空间的路径, 目的节点的网络命名空间的路径
        """
        source_net_namespace_path = f"/var/run/netns/{self.source_node.pid}"
        dest_net_namespace_path = f"/var/run/netns/{self.dest_node.pid}"
        return source_net_namespace_path, dest_net_namespace_path

    def get_source_and_dest_ip(self) -> (str, str):
        source_ip = self.source_node_interface_address
        dest_ip = self.dest_node_interface_address
        return source_ip, dest_ip

    def generate_single_actual_link(self):
        """
        使用 veth pair 生成一条实际链路
        """
        source_veth_name, dest_veth_name = self.get_source_and_dest_veth_names()
        source_net_ns_path, dest_net_ns_path = self.get_source_and_dest_net_namespace_path()
        source_ip, dest_ip = self.get_source_and_dest_ip()
        ip = IPRoute()
        ip.link("add", ifname=source_veth_name, peer=dest_veth_name, kind="veth")
        ip.link("set", index=ip.link_lookup(ifname=source_veth_name)[0], net_ns_fd=source_net_ns_path)
        ip.link("set", index=ip.link_lookup(ifname=dest_veth_name)[0], net_ns_fd=dest_net_ns_path)
        with NetNS(source_net_ns_path) as ns:
            idx = ns.link_lookup(ifname=source_veth_name)[0]
            ns.addr("add", index=idx, address=source_ip[:-3], prefixlen=30)
            ns.link("set", index=idx, state="up")
        with NetNS(dest_net_ns_path) as ns:
            idx = ns.link_lookup(ifname=dest_veth_name)[0]
            ns.addr("add", index=idx, address=dest_ip[:-3], prefixlen=30)
            ns.link("set", index=idx, state="up")
        ip.close()

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
