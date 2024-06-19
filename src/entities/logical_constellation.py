if __name__ == "__main__":
    import sys

    sys.path.append("../")
import functools
from src.config import config_loader as clm
from src.entities import node as nm
from src.entities import satellite as sm
from src.tools.network import subnet_generator as sgm
from src.entities import link as lm
from typing import List, Mapping
from src.entities import lir_link_identifier as llim


class LogicalConstellation:

    def __init__(self, config_loader: clm.ConfigLoader):
        """
        进行星座的初始化
        """
        self.config_loader = config_loader
        self.subnet_generator = sgm.SubnetGenerator.generate_subnets()

        self.satellites: List[sm.Satellite] = []
        self.isls: List[lm.Link] = []  # ISL 集合 (不含方向)
        self.lir_link_identifiers: List[llim.LiRLinkIdentifier] = []  # 链路标识集合 (含方向)
        self.map_from_source_dest_pair_to_lir_link_identifier: Mapping[(int, int): llim.LiRLinkIdentifier] = {}

        self.generate_satellites()
        self.generate_isls()

    def generate_satellites(self):
        """
        生成在星座之中的卫星
        :return:
        """
        num_of_orbit = self.config_loader.num_of_orbit
        sat_per_orbit = self.config_loader.sat_per_orbit
        # 遍历所有的轨道编号(0 ~ num_of_orbit-1)
        for orbit_index in range(num_of_orbit):
            for sat_index in range(sat_per_orbit * orbit_index, sat_per_orbit * (orbit_index + 1)):
                sat_index_in_orbit = sat_index % sat_per_orbit
                satellite = sm.Satellite(node_index=sat_index, node_type=nm.Node.Type.SATELLITE_NODE,
                                         orbit_index=orbit_index, sat_index_in_orbit=sat_index_in_orbit)
                self.satellites.append(satellite)

    def generate_isls(self):
        for satellite in self.satellites:
            self.generate_intra_orbit_isl(satellite)
            self.generate_inter_orbit_isl(satellite)

    def generate_inter_orbit_isl(self, satellite: sm.Satellite):
        """
        生成异轨星间链路
        :param satellite: 卫星
        """
        num_of_orbit = self.config_loader.num_of_orbit
        sat_per_orbit = self.config_loader.sat_per_orbit

        if satellite.orbit_index + 1 < num_of_orbit:
            source_sat_orbit_index = satellite.orbit_index
            source_sat_index_in_orbit = satellite.sat_index_in_orbit
            source_sat_index = satellite.node_index

            dest_sat_orbit_index = source_sat_orbit_index + 1  # 异轨道
            dest_sat_index_in_orbit = source_sat_index_in_orbit  # 同轨内编号
            dest_sat_index = dest_sat_orbit_index * sat_per_orbit + dest_sat_index_in_orbit

            self.generate_isl_and_two_lir_link_identifiers(source_sat_index, dest_sat_index)
        else:
            pass  # 反向缝不建立连接

    def generate_intra_orbit_isl(self, satellite: sm.Satellite):
        """
        生成同轨道星间链路
        :param satellite 卫星
        """
        sat_per_orbit = self.config_loader.sat_per_orbit

        source_sat_orbit_index = satellite.orbit_index
        source_sat_index_in_orbit = satellite.sat_index_in_orbit
        source_sat_index = satellite.node_index

        dest_sat_orbit_index = source_sat_orbit_index  # 同轨道
        dest_sat_index_in_orbit = (source_sat_index_in_orbit + 1) % sat_per_orbit  # 不同轨内编号
        dest_sat_index = dest_sat_orbit_index * sat_per_orbit + dest_sat_index_in_orbit

        if source_sat_index_in_orbit == dest_sat_index_in_orbit:
            pass  # 对应于轨道只有一颗卫星的情况
        else:
            self.generate_isl_and_two_lir_link_identifiers(source_sat_index, dest_sat_index)

    def generate_isl_and_two_lir_link_identifiers(self, source_sat_index: int, dest_sat_index: int):
        """
        生成 isl 以及两个 lir 链路标识
        :param source_sat_index: 源卫星 index
        :param dest_sat_index: 目的卫星 index
        :return:
        """
        source_sat = self.satellites[source_sat_index]
        dest_sat = self.satellites[dest_sat_index]

        current_isl_id = len(self.isls) + 1

        subnet, source_sat_address, dest_sat_address = next(self.subnet_generator)
        source_sat.connect_subnet_list.append(subnet)
        dest_sat.connect_subnet_list.append(subnet)
        source_sat.ip_addresses[source_sat.interface_index] = source_sat_address
        dest_sat.ip_addresses[dest_sat.interface_index] = dest_sat_address

        # --------------------------- 生成无方向链路 -------------------------
        isl = lm.Link(link_id=current_isl_id, source_node=source_sat,
                      source_node_interface_index=source_sat.interface_index,
                      source_node_interface_address=source_sat_address,
                      dest_node=dest_sat,
                      dest_node_interface_index=dest_sat.interface_index,
                      link_type=lm.Link.Type.INTER_SATELLITE_LINK,
                      dest_node_interface_address=dest_sat_address)

        self.isls.append(isl)
        # --------------------------- 生成无方向链路 -------------------------
        # ----------------------- 生成双方向lir链路标识 -----------------------
        current_link_identifier_id = len(self.lir_link_identifiers) + 1
        forward_identifier = llim.LiRLinkIdentifier(link_identifier_id=current_link_identifier_id,
                                                    source_node=source_sat,
                                                    source_interface_index=source_sat.interface_index,
                                                    dest_node=dest_sat)
        self.lir_link_identifiers.append(forward_identifier)
        source_sat.link_identifiers.append(forward_identifier)
        self.map_from_source_dest_pair_to_lir_link_identifier[
            (source_sat_index, dest_sat_index)] = forward_identifier

        current_link_identifier_id = len(self.lir_link_identifiers) + 1
        reverse_identifier = llim.LiRLinkIdentifier(link_identifier_id=current_link_identifier_id,
                                                    source_node=dest_sat,
                                                    source_interface_index=dest_sat.interface_index,
                                                    dest_node=source_sat)
        self.lir_link_identifiers.append(reverse_identifier)
        dest_sat.link_identifiers.append(reverse_identifier)
        self.map_from_source_dest_pair_to_lir_link_identifier[
            (dest_sat_index, source_sat_index)] = reverse_identifier
        # ----------------------- 生成双方向lir链路标识 -----------------------

        source_sat.interface_index += 1
        dest_sat.interface_index += 1

    def satellites_in_str(self) -> str:
        """
        :return: 星座之中所有卫星的字符串表示
        """
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", [str(satellite) for satellite in self.satellites])

    def isls_in_str(self) -> str:
        """
        :return: 星座之中所有的星间链路的字符串表示
        """
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", [str(isl) for isl in self.isls])

    def lir_identifiers_in_str(self) -> str:
        """
        :return: 星座之中所有链路标识的字符串表示
        """
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", [str(isl) for isl in self.lir_link_identifiers])


if __name__ == "__main__":
    config_loader_tmp = clm.ConfigLoader()
    config_loader_tmp.load()
    print(config_loader_tmp)
    logical_constellation = LogicalConstellation(config_loader=config_loader_tmp)
    print(logical_constellation.satellites_in_str())
    print(logical_constellation.isls_in_str())
    print(logical_constellation.lir_identifiers_in_str())
    print(len(logical_constellation.lir_link_identifiers))
