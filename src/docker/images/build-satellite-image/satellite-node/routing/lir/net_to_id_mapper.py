from routing.lir import netlink_client as ncm


class NetNamespaceToNodeIdMapper:
    def __init__(self, netlink_client: ncm.NetlinkClient, node_id: str):
        """
        将卫星的命名空间和 id 绑定在一起
        """
        self.netlink_client = netlink_client
        self.node_id = node_id

    def start(self):
        """
        让网络命名空间能知道，当前的节点的 id 是什么
        :return:
        """
        self.netlink_client.send_netlink_data(self.node_id, ncm.NetlinkMessageType.CMD_BIND_NET_TO_SAT_NAME)
