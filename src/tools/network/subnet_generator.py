import ipaddress


class SubnetGenerator:
    @classmethod
    def generate_subnets(cls, base_network_address: str = "192.168.0.0/16"):
        """
        :param base_network_address: 网络地址块
        :return: (子网, pointToPoint 链路的第一个地址, pointToPoint 链路的第二个地址)
        """
        base_network = ipaddress.ip_network(base_network_address)
        for single_subnet in base_network.subnets(new_prefix=30):
            split_part = str(single_subnet)[:-3].split(".")
            split_part[3] = str(int(split_part[3]) + 1)
            first_host_address = ".".join(split_part)
            split_part[3] = str(int(split_part[3]) + 1)
            second_host_address = ".".join(split_part)
            yield single_subnet, f"{first_host_address}/30", f"{second_host_address}/30"


if __name__ == "__main__":
    for item in SubnetGenerator.generate_subnets():
        print(item)
