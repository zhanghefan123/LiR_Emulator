from typing import List
from src.entities import satellite as sm


class IPtoIDGenerator:
    def __init__(self, satellites: List[sm.Satellite], generate_destination: str):
        self.satellites = satellites
        self.generate_destination = generate_destination

    def generate(self):
        full_str = ""
        for satellite in self.satellites:
            ip_addresses = "|".join(satellite.ip_addresses.values())
            id_to_ip_mapping_str = f"{satellite.container_name}|{ip_addresses}"
            full_str += id_to_ip_mapping_str
        with open(f"{self.generate_destination}/address_mapping.conf") as f:
            f.write(full_str)