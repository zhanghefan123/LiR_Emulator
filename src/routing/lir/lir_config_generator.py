from src.entities import satellite as sm
from typing import List


class LirConfigGenerator:
    def __init__(self, satellites: List[sm.Satellite], generate_destination: str):
        """
        初始化 lir 配置生成器
        :param satellites: 所有的卫星
        :param generate_destination: 生成 lir 的位置
        """
        self.satellites = satellites
        self.generate_destination = generate_destination

    def generate(self):
        """
        进行 lir 配置的生成
        """
        for satellite in self.satellites:
            prefix = satellite.node_type.get_prefix()
            lir_file_path = f"{self.generate_destination}/{satellite.container_name}.conf"
            with open(lir_file_path, "w") as f:
                full_str = ""
                for interface_index, lir_link_identifier in enumerate(satellite.link_identifiers):
                    full_str += f"{prefix}{satellite.node_id}_index{interface_index + 1}->{lir_link_identifier.link_identifier_id}\n"
                f.write(full_str)
