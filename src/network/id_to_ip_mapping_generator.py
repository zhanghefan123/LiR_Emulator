from typing import List
from src.entities import satellite as sm


class IPtoIDGenerator:
    def __init__(self, satellites: List[sm.Satellite], generate_destination: str):
        self.satellites = satellites
        self.generate_destination = generate_destination

    def generate(self):
        full_str = ""
        for index, satellite in enumerate(self.satellites):
            if index == len(self.satellites) - 1:
                # 到达最后一行不需要加 \n
                ip_addresses = "|".join(satellite.ip_addresses.values())
                id_to_ip_mapping_str = f"{satellite.container_name}|{ip_addresses}"
            else:
                # 未到达最后一行需要加 \n
                ip_addresses = "|".join(satellite.ip_addresses.values())
                id_to_ip_mapping_str = f"{satellite.container_name}|{ip_addresses}\n"
            full_str += id_to_ip_mapping_str
        with open(f"{self.generate_destination}/address_mapping.conf", "w") as f:
            f.write(full_str)
