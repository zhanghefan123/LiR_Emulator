import networkx as nx
from typing import List, Dict, Tuple
from src.entities import satellite as sm
from src.entities import lir_link_identifier as llim


class LirRouteCalculator:
    def __init__(self, satellites: List[sm.Satellite],
                 lir_link_identifiers: List[llim.LiRLinkIdentifier],
                 map_from_source_dest_pair_to_lir_link_identifier: Dict[Tuple[int, int], llim.LiRLinkIdentifier],
                 generate_destination: str):
        """
        初始化路由配置生成器
        :param satellites: 所有的卫星
        :param lir_link_identifiers: 所有的 lir 链路标识
        :param generate_destination: 生成路由的地址
        """
        self.satellites = satellites
        self.lir_link_identifiers = lir_link_identifiers
        self.map_from_source_dest_pair_to_lir_link_identifier = map_from_source_dest_pair_to_lir_link_identifier
        self.generate_destination = generate_destination
        self.topology_direction_graph = nx.Graph()

    def generate(self):
        """
        生成路由文件
        """
        satellite_ids = [satellite.node_id for satellite in self.satellites]
        source_dest_pair = [(link_identifier.source_node.node_id, link_identifier.dest_node.node_id, 1)
                            for link_identifier in self.lir_link_identifiers]
        self.topology_direction_graph.add_nodes_from(satellite_ids)
        self.topology_direction_graph.add_weighted_edges_from(source_dest_pair)

        all_sat_route_str = ""
        for satellite in self.satellites:
            single_sat_route_in_str = self.calculate_satellite_routes_to_others(satellite.node_id)
            single_sat_route_file_generate_destination = f"{self.generate_destination}/{satellite.container_name}.conf"
            with open(single_sat_route_file_generate_destination, "w") as f:
                f.write(single_sat_route_in_str)
            all_sat_route_str += single_sat_route_in_str
        all_sat_route_file_generate_destination = f"{self.generate_destination}/all.conf"
        with open(all_sat_route_file_generate_destination, "w") as f:
            f.write(all_sat_route_file_generate_destination)

    def calculate_satellite_routes_to_others(self, selected_satellite_id: int) -> str:
        """
        计算某个卫星到其他卫星的路由的字符串表示
        :param 选中的某颗卫星
        :return: 计算的到其他节点的路由的字符串表示
        """
        # --------------------------- 记录 Map<目的节点, 链路标识路径> ---------------------------
        identifier_sequence_to_other_satellites: Dict[int, List[int]] = {}
        node_sequence_to_other_satellites: Dict[int, List[int]] = {}
        satellite_ids = [satellite.node_id for satellite in self.satellites]
        for satellite_id in satellite_ids:
            if selected_satellite_id == satellite_id:
                continue
            else:
                node_sequence = nx.shortest_path(self.topology_direction_graph, source=selected_satellite_id, target=satellite_id)
                identifier_sequence = [self.map_from_source_dest_pair_to_lir_link_identifier[(node_sequence[index], node_sequence[index+1])]
                                       for index in range(len(node_sequence) - 1)]
                identifier_sequence_to_other_satellites[satellite_id] = identifier_sequence
                node_sequence_to_other_satellites[satellite_id] = node_sequence[1:]
        # --------------------------- 记录 Map<目的节点, 链路标识路径> ---------------------------
        # ------------------------------- 根据 Map 进行路径的生成 -------------------------------
        all_routes_str = ""
        for dest_satellite_id in identifier_sequence_to_other_satellites.keys():
            identifier_sequence = identifier_sequence_to_other_satellites[dest_satellite_id]
            node_sequence = node_sequence_to_other_satellites[dest_satellite_id]
            length_of_identifier_sequence = len(identifier_sequence)
            sequence_str = ""
            for index in range(len(identifier_sequence)):
                if index != length_of_identifier_sequence:
                    # 为了进行路径验证，我们不仅要插入链路标识还需要插入节点标识
                    sequence_str += f"{identifier_sequence[index]}->{node_sequence[index]}->"
                else:
                    sequence_str += f"{identifier_sequence[index]}->{node_sequence}->"
            single_route_str = f"source:{selected_satellite_id} dest:{dest_satellite_id} {sequence_str}\n"
            all_routes_str += single_route_str
        return all_routes_str
        # ------------------------------- 根据 Map 进行路径的生成 -------------------------------


