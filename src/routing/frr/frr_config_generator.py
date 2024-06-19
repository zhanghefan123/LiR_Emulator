import os.path
from src.entities import satellite as sm
from typing import List


class FrrConfigGenerator:
    def __init__(self, satellites: List[sm.Satellite], generate_destination: str):
        """
        初始化 frr 配置生成器
        :param satellites: 所有的卫星
        :param generate_destination: 生成 frr 的位置
        """
        self.satellites = satellites
        self.generate_destination = generate_destination

    def generate(self):
        """
        进行 frr 配置的生成
        """
        if not os.path.exists(self.generate_destination):
            os.system(f"mkdir -p {self.generate_destination}")
        else:
            for satellite in self.satellites:
                prefix = satellite.node_type.get_prefix()
                with open(f"{self.generate_destination}/{satellite.container_name}.conf", "w") as f:
                    full_str = f"""frr version 7.2.1 
frr defaults traditional
hostname satellite_{satellite.node_id}
log syslog informational
no ipv6 forwarding
service integrated-vtysh-config
!
router ospf
    redistribute connected
"""
                    for connected_subnet in satellite.connect_subnet_list:
                        full_str += f"\t network {connected_subnet} area 0.0.0.0\n"
                    full_str += "!\n"
                    full_str += "line vty\n"
                    full_str += "!\n"
                    f.write(full_str)


