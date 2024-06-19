from src.entities import node as nm


class Satellite(nm.Node):
    def __init__(self, node_index: int, node_type: nm.Node.Type,
                 orbit_index: int, sat_index_in_orbit: int):
        """
        进行卫星的初始化
        :param node_index: 节点的 id
        :param node_type: 节点的类型
        :param orbit_index: 轨道的编号
        :param sat_index_in_orbit: 卫星在轨道内的编号
        """
        super().__init__(node_index, node_type)
        self.orbit_index = orbit_index
        self.sat_index_in_orbit = sat_index_in_orbit
        self.link_identifiers = []

    def __str__(self):
        basic_node_str = super().__str__()
        return basic_node_str + f"orbit_index: {self.orbit_index} sat_index_in_orbit: {self.sat_index_in_orbit}"

