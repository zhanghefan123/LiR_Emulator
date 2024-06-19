from src.entities import satellite as sm


class LiRLinkIdentifier:
    def __init__(self, link_identifier_id: int, source_node: sm.Satellite,
                 source_interface_index: int, dest_node: sm.Satellite):
        """
        进行 Lipsin 链路标识的初始化
        :param link_identifier_id: 链路标识 id
        :param source_node: 源卫星
        :param source_interface_index 源卫星中和这个链路标识对应的接口
        :param dest_node: 目的卫星
        """
        self.link_identifier_id = link_identifier_id
        self.source_node = source_node
        self.source_interface_index = source_interface_index
        self.dest_node = dest_node

    def __str__(self):
        """
        将 LiR 链路标识对象转换为字符串
        """
        return f"link identifier id: {self.link_identifier_id} | [{self.source_node.container_name}]-->[{self.dest_node.container_name}]"
