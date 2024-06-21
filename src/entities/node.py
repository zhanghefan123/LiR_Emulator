from enum import Enum
from typing import Union


class Node:
    class Type(Enum):
        SATELLITE = 1
        GROUND_STATION = 2

        def __str__(self) -> Union[str, ValueError]:
            """
            节点的字符串表示
            :return:
            """
            if self.value == self.SATELLITE.value:
                return "satellite"
            elif self.value == self.GROUND_STATION.value:
                return "ground-station"
            else:
                return ValueError("unsupported entity type")

        def get_prefix(self) -> Union[str, ValueError]:
            if self.value == self.SATELLITE.value:
                return "sa"
            elif self.value == self.GROUND_STATION.value:
                return "gn"
            else:
                return ValueError("unsupported entity type")

    def resolve_container_name(self) -> str:
        if self.node_type.value == Node.Type.SATELLITE.value:
            container_name = f"satellite{self.node_id}"
        elif self.node_type.value == Node.Type.GROUND_STATION.value:
            container_name = f"ground-station{self.node_id}"
        else:
            raise ValueError("unsupported node type")
        return container_name

    def __init__(self, node_index: int, node_type: Type):
        """
        节点初始化方法
        :param node_index:
        :param node_type:
        """
        # -------- basic attr --------
        self.node_index = node_index
        self.node_id = self.node_index + 1
        self.node_type = node_type
        self.interface_index = 0
        self.ip_addresses = {}
        self.connect_subnet_list = []
        # -------- basic attr --------
        # ---- container related -----
        self.container_name = self.resolve_container_name()
        self.addr_connect_to_docker_zero = None
        self.container_id = None
        self.pid = None
        # ---- container related -----

    def __str__(self):
        return f"node_id: {self.node_id} node_type: {self.node_type} interface_index: {self.interface_index} "
